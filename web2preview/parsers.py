import re
import unicodedata
from urllib.parse import urlparse, urlunparse
from typing import Dict, List, Optional, Tuple

import requests
from requests.exceptions import *
from bs4 import BeautifulSoup

from .models import WebPreview
from .excepts import *
from .parsers import *
from .regex import VALID_URL, WHITESPACE


def extract_title(soup: BeautifulSoup) -> Optional[str]:
    """Extract title from the given web page."""
    # if title tag is present and has text in it, return it as the title
    if soup.title and soup.title.text:
        return soup.title.text

    # else if h1 tag is present and has text in it, return it as the title
    elif soup.h1 and soup.h1.text:
        return soup.h1.text

    return None


def extract_description(soup: BeautifulSoup) -> Optional[str]:
    """Extract description from the given web page."""

    def treat_candidate(candidate_text: str) -> str:
        text = candidate_text.strip()
        parts = [p.strip().rstrip(".") for p in text.split(".") if p.strip().rstrip(".")]
        desc = ". ".join(parts[:2]) + "."
        return desc

    # extract description from meta[name='description']
    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and meta_description["content"]:
        return meta_description["content"]

    # Class shortdescription
    short_description = soup.find("div", class_="shortdescription")
    if short_description and short_description.string:
        return short_description.string

    # else extract description from the first <p> sibling to the first <h1>
    first_h1 = soup.find("h1")
    if first_h1:
        first_ps = first_h1.find_all_next("p")
        for p_candidate in first_ps:
            if p_candidate and p_candidate.text and p_candidate.text.strip():
                return treat_candidate(p_candidate.text)

    # else extract description from the first <p>
    first_ps = soup.find_all("p")
    for p_candidate in first_ps:
        if p_candidate and p_candidate.text and p_candidate.text.strip():
            return treat_candidate(p_candidate.text)

    return None


def extract_image(soup: BeautifulSoup) -> Optional[str]:
    """Extract preview image from the given web page."""
    # extract the first image which is sibling to the first h1
    first_h1 = soup.find("h1")
    if first_h1:
        first_image = first_h1.find_next_sibling("img")
        if first_image and first_image["src"]:
            return first_image["src"]

    return None


def sanitize(value: str) -> str:
    """Sanitize given string.

    See:
    https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
    """
    # Do not process empty strings or None
    if not value:
        return value

    # First, remove all whitespace characters.
    v = re.sub(WHITESPACE, " ", value)
    # Now, normalize unicode symbols
    v = unicodedata.normalize("NFKD", v)

    return v


def extract_meta_attributes(
    soup: BeautifulSoup, target_attribute: str, properties: List[str]
) -> Dict[str, str]:
    """Extract social media meta properties."""
    attributes = {}
    # Different subtypes have different target_attribute:
    # - OpengGraph has <meta property="" content="">
    # - TwitterCard  has <meta name="" content="">
    # - Google+  has <meta itemprop="" content="">
    for p in properties:
        meta = soup.find("meta", attrs={target_attribute: p})

        # turn "og:title" to "title" and "og:price:amount" to price_amount
        if re.search(r":", p):
            prop = p.split(":", 1)[1].replace(":", "_")

        # turn "camelCase" to "camel_case"
        elif re.search(r"[A-Z]", p):
            # regex taken from 2nd answer at
            # http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
            prop = re.sub("(?!^)([A-Z]+)", r"_\1", p).lower()
        else:
            prop = p

        attributes[prop] = meta["content"] if meta and meta["content"] else None

    return attributes


def make_absolute_url(url: str, base_url: str) -> Optional[str]:
    """Converts given url to absolute url using parts from base_url if necessary."""

    # Empty URLs are returned as is
    if not url or not base_url:
        return url

    base = urlparse(base_url)
    parsed = urlparse(url)

    # If the URL is not absolute, then we append its
    # path, params, query, and fragment to the scheme + netloc
    # of the base url
    url_components = [
        (parsed.scheme if parsed.netloc else base.scheme) or "http",
        parsed.netloc or base.netloc,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    ]

    return urlunparse(url_components)


def retrieve_content(
    url: str, timeout: Optional[int] = None, headers: Optional[Dict[str, str]] = None
) -> str:
    try:
        res = requests.get(url, timeout=timeout, headers=headers)
    except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
        raise URLUnreachable("The URL is unreachable.")

    if res.status_code == 404:
        raise URLNotFound("The web page does not exist.")

    return res.text


def initialize(
    url: str,
    timeout: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    content: Optional[str] = None,
    target_attribute: Optional[str] = None,
    properties: Optional[List[str]] = None,
    parser: str = "html.parser",
) -> Tuple[str, str, BeautifulSoup]:
    if not url:
        raise EmptyURL("Please pass a valid URL as the first argument.")

    m = VALID_URL.match(url)
    if not m:
        raise InvalidURL("The URL is invalid.")

    if not m.group("domain"):
        raise URLUnreachable("URL is unreacheable.")

    if not m.group("scheme"):
        url = f"http://{url}"

    if not content:
        content = retrieve_content(url=url, timeout=timeout, headers=headers)

    if (target_attribute or properties) and not (target_attribute and properties):
        raise EmptyProperties("Both target_attribute and meta_properties must be specified")

    soup = BeautifulSoup(content, parser)

    return url, content, soup


def parse_generic(soup: BeautifulSoup, url: str, absolute_url: bool = False) -> WebPreview:
    title = sanitize(extract_title(soup))
    description = sanitize(extract_description(soup))
    image = extract_image(soup)

    if absolute_url and image:
        image = make_absolute_url(image, url)

    result = WebPreview(url=url, title=title, description=description, image=image)
    return result


def parse_meta(
    soup: BeautifulSoup,
    url: str,
    target_attribute: str,
    properties: List[str],
    absolute_url: bool = False,
) -> WebPreview:
    props = extract_meta_attributes(soup, target_attribute, properties)

    image = props.get("image")
    if absolute_url and image:
        image = make_absolute_url(image, url)
        props["image"] = image

    result = WebPreview(**props)
    return result


def parse_open_graph(
    soup: BeautifulSoup,
    url: str,
    properties: Optional[List[str]] = None,
    absolute_url: bool = False,
) -> WebPreview:
    if not properties:
        properties = ["og:title", "og:description", "og:image"]
    result = parse_meta(soup, url, "property", properties, absolute_url)
    return result


def parse_twitter_card(
    soup: BeautifulSoup,
    url: str,
    properties: Optional[List[str]] = None,
    absolute_url: bool = False,
) -> WebPreview:
    if not properties:
        properties = ["twitter:title", "twitter:description", "twitter:image"]
    result = parse_meta(soup, url, "name", properties, absolute_url)
    return result


def parse_schema(
    soup: BeautifulSoup,
    url: str,
    properties: Optional[List[str]] = None,
    absolute_url: bool = False,
) -> WebPreview:
    if not properties:
        properties = ["name", "description", "image"]
    result = parse_meta(soup, url, "itemprop", properties, absolute_url)
    if result.name:
        result["title"] = result.name
    return result


def web2preview(
    url: str,
    timeout: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    content: Optional[str] = None,
    target_attribute: Optional[str] = None,
    properties: Optional[List[str]] = None,
    parser: str = "html.parser",
    absolute_url: bool = False,
) -> WebPreview:
    """Extract title, description and image from any page.

    This method follows a fallback mechanism, by trying one approach after another.
    It starts with user supplied ``target_attribute`` and ``properties``, then
    attempts standard OpenGraph tags, followed by TwitterCard and Schema tags.
    As a last resort, the page is treated as a generic webpage.

    If at any moment all three of title, description, and preview image are extracted
    the result is returned without trying anything further.

    Args:
        url (str): URL of the page. If content is supplied, the URL will not be
            requested but can still be used to convert relative URLs of the image
            to absolute one.
        timeout (int): Timeout in seconds for requests library to wait before throwing
            a timeout exception when requesting the page's source.
        headers (dict): Request headers to pass to the requests library.
        content (str): Page's content. When given, no request will be made to retrieve
            the source and instead the supplied content will be used.
        target_attribute (str): Manually specify which meta tag attribute to parse
            as a source of properties.
        properties (list): Manually specify which meta tag properties to parse. Must be
            specified together with ``target_attribute``.
        parser (str): Which parser type to give to BeautifulSoup library. Allowed values
            are "html.parser", "lxml", "html5lib". Note all of them except for "html.parser"
            require additional dependencies. Defaults to "html.parser".
        absolute_url (bool): Convert preview image URL to absolute URL. Defaults to False.

    Returns:
        WebPreview: object with extracted fields.
    """

    url, _, soup = initialize(url, timeout, headers, content, target_attribute, properties, parser)
    result = WebPreview(url=url)

    # If explicit list of meta properties is given, try to extract data using them
    if target_attribute and properties:
        meta = parse_meta(soup, url, target_attribute, properties, absolute_url)
        result.merge(meta)
        if result.is_complete():
            return result

    # Try to extract standard OpenGraph meta properties
    open_graph = parse_open_graph(soup, url, properties, absolute_url)
    result.merge(open_graph)
    if result.is_complete():
        return result

    # Try to extract Twitter Card properties
    twitter_card = parse_twitter_card(soup, url, properties, absolute_url)
    result.merge(twitter_card)
    if result.is_complete():
        return result

    # Try to extract Schema properties
    schema = parse_schema(soup, url, properties, absolute_url)
    result.merge(schema)
    if result.is_complete():
        return result

    # Try to extract from generic webpage
    generic = parse_generic(soup, url, absolute_url)
    result.merge(generic)
    return result
