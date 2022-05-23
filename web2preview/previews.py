"""Previews module.

Compatibility layer with original webpreview library.
"""

from .excepts import *
from .parsers import *
from .models import WebPreview
from .previews import web2preview


class PreviewBase(WebPreview):
    """
    Base for all compatibility web previews.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        properties: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
        target_attribute: str = "property",
    ):
        if not url:
            raise EmptyURL("Please pass a valid URL as the first argument.")

        _url, _, soup = initialize(
            url, timeout, headers, content, target_attribute, properties, parser
        )

        if not properties:
            raise EmptyProperties("Please pass list of properties to be extracted.")

        super().__init__(
            url=url,
            properties=properties,
            timeout=timeout,
            headers=headers,
            content=content,
            parser=parser,
        )

        # These two properties below are for compatibility with these old classes from webpreview
        self.url = _url
        self.properties = properties
        self._soup = soup


class GenericPreview(PreviewBase):
    """
    Extracts title, description, image from a webpage's body instead of the meta tags.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        properties: Optional[List[str]] = ["title", "description", "image"],
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ):
        super().__init__(url, properties, timeout, headers, content, parser)
        preview = parse_generic(self._soup, self.url)
        self.merge(preview)


class SocialPreviewBase(PreviewBase):
    """
    Abstract class for OpenGraph, TwitterCard and Google+.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        properties: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
        target_attribute: str = "property",
    ):
        super().__init__(url, properties, timeout, headers, content, parser)
        preview = parse_meta(self._soup, self.url, target_attribute, properties)
        self.merge(preview)


class OpenGraph(SocialPreviewBase):
    """
    Gets OpenGraph meta properties of a webpage.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        properties: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ):
        super().__init__(url, properties, timeout, headers, content, parser)
        preview = parse_open_graph(self._soup, self.url, properties)
        self.merge(preview)


class TwitterCard(SocialPreviewBase):
    """
    Gets TwitterCard meta properties of a webpage.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        properties: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ):
        super().__init__(url, properties, timeout, headers, content, parser)
        preview = parse_twitter_card(self._soup, self.url, properties)
        self.merge(preview)


class Schema(SocialPreviewBase):
    """
    Gets Schema meta properties from a website.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        properties: Optional[List[str]] = None,
        timeout: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
        parser: str = "html.parser",
    ):
        super().__init__(url, properties, timeout, headers, content, parser)
        preview = parse_schema(self._soup, self.url, properties)
        self.merge(preview)


def web_preview(
    url: Optional[str] = None,
    timeout: Optional[int] = None,
    headers: Optional[Dict[str, str]] = None,
    content: Optional[str] = None,
    parser: str = "html.parser",
    absolute_image_url: bool = False,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Extract title, description and image from OpenGraph or TwitterCard or Schema or GenericPreview.

    This function is maintained for compatibility purposes with ``webpreview`` library and is simply
    a wrapper around the newer ``web2preview`` function.
    For direct and convenient access to the parsing results through the ``WebPreview`` object
    use the newer ``web2preview`` function.

    Args:
        url (str): URL of the page. If content is supplied, the URL will not be
            requested but can still be used to convert relative URLs of the image
            to absolute one.
        timeout (int): Timeout in seconds for requests library to wait before throwing
            a timeout exception when requesting the page's source.
        headers (dict): Request headers to pass to the requests library.
        content (str): Page's content. When given, no request will be made to retrieve
            the source and instead the supplied content will be used.
        parser (str): Which parser type to give to BeautifulSoup library. Allowed values
            are "html.parser", "lxml", "html5lib". Note all of them except for "html.parser"
            require additional dependencies. Defaults to "html.parser".
        absolute_image_url (bool): Convert preview image URL to absolute URL. Defaults to False.

    Returns:
        Tuple of 3 strings: title, description, image all of which can be None.
    """

    preview = web2preview(url, timeout, headers, content, None, None, parser, absolute_image_url)
    return preview.title, preview.description, preview.image
