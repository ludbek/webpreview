from bs4 import BeautifulSoup
import requests
import re

class EmptyURL(Exception):
    """
    Exception for empty URL.
    """
    pass

class InvalidURL(Exception):
    """
    Exception for invalid URL.
    """
    pass


class PreviewBase(object):
    """
    Base for all web preview.
    """
    def __init__(self, url = None, config = ['title', 'desc', 'img']):
        # if no first argument raise URL required exception
        if not url:
            raise EmptyURL("Please pass a valid URL as the first argument.")
        # raise invalid url exception for invalid URL
        # taken from django https://github.com/django/django/blob/master/django/core/validators.py#L68
        valid_url = re.compile(
            r'^(https?://)?'  # scheme is validated separately
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not valid_url.match(url):
            raise InvalidURL("The URL is invalid.")

        # its safe to assign the url and config
        self.url = url
        self.config = config


class GenericPreview(PreviewBase):
    pass
