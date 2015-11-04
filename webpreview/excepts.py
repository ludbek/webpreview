class WebpreviewException(Exception):
    """
    Base Webpreview Exception.
    """
    pass


class EmptyURL(WebpreviewException):
    """
    WebpreviewException for empty URL.
    """
    pass


class EmptyProperties(WebpreviewException):
    """
    WebpreviewException for empty properties.
    """
    pass


class URLNotFound(WebpreviewException):
    """
    WebpreviewException for 404 URLs.
    """
    pass


class URLUnreachable(WebpreviewException):
    """
    WebpreviewException for 404 URLs.
    """
    pass
