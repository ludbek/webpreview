import re
from urllib.parse import urlparse, urlunparse
from typing import Dict, List, Optional, Tuple

import requests
from requests.exceptions import *
from bs4 import BeautifulSoup

from .exceptions import *


class PreviewBase:
    """Base for all web preview."""

    def __init__(
        self,
        url: str,
        properties: List[str] = [],
        timeout: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ) -> None:
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.image: Optional[str] = None
        self.name: Optional[str] = None

        # if no first argument raise URL required exception
        if not url:
            raise EmptyURL("Please pass a valid URL as the first argument.")

        scheme, netloc, _, _, _, _ = urlparse(url)

        # if no schema add http as default
        if not netloc:
            raise URLUnreachable("The URL does not exist.")

        if not scheme:
            scheme = "http"

        # if content is provided don't fetch from url
        if not content:
            content = PreviewBase.get_content(url, timeout, headers)

        # its safe to assign the url
        self.url = url

        if not properties:
            raise EmptyProperties("Please pass list of properties to be extracted.")

        # its safe to assign properties
        self.properties = properties
        self._soup = BeautifulSoup(content, parser)

    @staticmethod
    def get_content(
        url: str, timeout: Optional[int] = None, headers: Optional[Dict[str, str]] = None
    ) -> str:
        try:
            res = requests.get(url, timeout=timeout, headers=headers)
        except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
            raise URLUnreachable("The URL is unreachable.")

        if res.status_code == 404:
            raise URLNotFound("The web page does not exist.")

        return res.text


class GenericPreview(PreviewBase):
    """Extracts title, description, image from a webpage's body instead of the meta tags."""

    def __init__(
        self,
        url: str,
        properties: List[str] = ["title", "description", "image"],
        timeout: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ) -> None:
        super(GenericPreview, self).__init__(
            url=url,
            properties=properties,
            timeout=timeout,
            headers=headers,
            content=content,
            parser=parser,
        )
        self.title = self._get_title()
        self.description = self._get_description()
        self.image = self._get_image()

    def _get_title(self) -> Optional[str]:
        """Extract title from the given web page."""

        soup = self._soup
        # if title tag is present and has text in it, return it as the title
        if soup.title and soup.title.text:
            return soup.title.text

        # else if h1 tag is present and has text in it, return it as the title
        if soup.h1 and soup.h1.text:
            return soup.h1.text

        # if no title, h1 return None
        return None

    def _get_description(self) -> Optional[str]:
        """Extract description from the given web page."""

        soup = self._soup
        # extract description from meta[name='description']
        meta_description = soup.find("meta", attrs={"name": "description"})
        if meta_description and meta_description["content"]:
            return meta_description["content"]

        # else extract description from the first <p> sibling to the first <h1>
        first_h1 = soup.find("h1")
        if first_h1:
            first_p = first_h1.find_next("p")
            if first_p and first_p.string:
                return first_p.text

        # else extract description from the first <p>
        first_p = soup.find("p")
        if first_p and first_p.string:
            return first_p.string

        # else
        return None

    def _get_image(self) -> Optional[str]:
        """Extract preview image from the given web page."""

        soup = self._soup
        # extract the first image which is sibling to the first h1
        first_h1 = soup.find("h1")
        if first_h1:
            first_image = first_h1.find_next_sibling("img")
            if first_image and first_image["src"]:
                return first_image["src"]

        return None


class SocialPreviewBase(PreviewBase):
    """Abstract class for OpenGraph, TwitterCard and Google+."""

    def __init__(
        self,
        url: str,
        target_attribute: str,
        properties: List[str] = [],
        timeout: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ) -> None:
        # Different subtypes have different target_attribute:
        # - OpengGraph has <meta property="" content="">
        # - TwitterCard  has <meta name="" content="">
        # - Google+  has <meta itemprop="" content="">
        self._target_attribute = target_attribute
        super().__init__(
            url=url,
            properties=properties,
            timeout=timeout,
            headers=headers,
            content=content,
            parser=parser,
        )

        soup = self._soup
        for property in self.properties:
            property_meta = soup.find("meta", attrs={self._target_attribute: property})

            # turn "og:title" to "title" and "og:price:amount" to price_amount
            if re.search(r":", property):
                new_property = property.split(":", 1)[1].replace(":", "_")

            # turn "camelCase" to "camel_case"
            elif re.search(r"[A-Z]", property):
                # regex taken from 2nd answer at
                # http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
                new_property = re.sub("(?!^)([A-Z]+)", r"_\1", property).lower()
            else:
                new_property = property

            if property_meta and property_meta["content"]:
                # dynamically attach property to instance
                self.__dict__[new_property] = property_meta["content"]
            else:
                self.__dict__[new_property] = None


class OpenGraph(SocialPreviewBase):
    """Gets OpenGraph meta properties of a webpage."""

    def __init__(
        self,
        url: str,
        properties: List[str] = ["og:title", "og:description", "og:image"],
        timeout: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ) -> None:
        super().__init__(
            url=url,
            target_attribute="property",
            properties=properties,
            timeout=timeout,
            headers=headers,
            content=content,
            parser=parser,
        )


class TwitterCard(SocialPreviewBase):
    """Gets TwitterCard meta properties of a webpage."""

    def __init__(
        self,
        url: str,
        properties: List[str] = ["twitter:title", "twitter:description", "twitter:image"],
        timeout: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ) -> None:
        super().__init__(
            url=url,
            target_attribute="name",
            properties=properties,
            timeout=timeout,
            headers=headers,
            content=content,
            parser=parser,
        )


class Schema(SocialPreviewBase):
    """Gets Schema meta properties from a website."""

    def __init__(
        self,
        url: str,
        properties: List[str] = ["name", "description", "image"],
        timeout: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ) -> None:
        super().__init__(
            url=url,
            target_attribute="itemprop",
            properties=properties,
            timeout=timeout,
            headers=headers,
            content=content,
            parser=parser,
        )


def webpreview(
    url: str,
    timeout: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    content: Optional[str] = None,
    parser: str = "html.parser",
    absolute_image_url: bool = False,
) -> PreviewBase:
    """Extract title, description and image from OpenGraph or TwitterCard or Schema or GenericPreview.

    Returns Preview object.
    """

    og = OpenGraph(url=url, timeout=timeout, headers=headers, content=content, parser=parser)
    if og.title:
        og.image = process_image_url(url, og.image, absolute_image_url)
        return og

    tc = TwitterCard(url=url, timeout=timeout, headers=headers, content=content, parser=parser)
    if tc.title:
        tc.image = process_image_url(url, tc.image, absolute_image_url)
        return tc

    s = Schema(url=url, timeout=timeout, headers=headers, content=content, parser=parser)
    if s.name:
        s.image = process_image_url(url, s.image, absolute_image_url)
        s.title = s.name
        return s

    gp = GenericPreview(url=url, timeout=timeout, headers=headers, content=content, parser=parser)
    gp.image = process_image_url(url, gp.image, absolute_image_url)
    return gp


def web_preview(
    url: str,
    timeout: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    content: Optional[str] = None,
    parser: str = "html.parser",
    absolute_image_url: bool = False,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Extract title, description and image from OpenGraph or TwitterCard or Schema or GenericPreview.

    Returns a tuple of title, description, and image url.
    """

    p = webpreview(
        url=url,
        timeout=timeout,
        headers=headers,
        content=content,
        parser=parser,
        absolute_image_url=absolute_image_url,
    )
    return p.title, p.description, p.image


def process_image_url(
    url: str, image_url: str, force_absolute_url: bool = False
) -> Optional[str]:
    # Empty Image URLs are returned as is
    if not image_url:
        return image_url

    if not force_absolute_url:
        return image_url

    parsed_url = urlparse(url)
    parsed_image_url = urlparse(image_url)

    # If the image URL is not absolute, then we append its
    # path, params, query, and fragment to the scheme + netloc
    # of the base url
    if not parsed_image_url.netloc:
        url_components = [
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_image_url.path,
            parsed_image_url.params,
            parsed_image_url.query,
            parsed_image_url.fragment,
        ]
    else:
        url_components = [
            parsed_image_url.scheme or "http",
            parsed_image_url.netloc,
            parsed_image_url.path,
            parsed_image_url.params,
            parsed_image_url.query,
            parsed_image_url.fragment,
        ]

    return urlunparse(url_components)
