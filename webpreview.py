from bs4 import BeautifulSoup
import requests
from requests.exceptions import *
import re

class EmptyURL(Exception):
    """
    Exception for empty URL.
    """
    pass


class URLNotFound(Exception):
    """
    Exception for 404 URLs.
    """
    pass


class URLUnreachable(Exception):
    """
    Exception for 404 URLs.
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

        # if no schema add http as default
        try:
            res = requests.get(url)
        except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
            raise URLUnreachable("The URL does not exists.")
        except MissingSchema: # if no schema add http as default
            url = "http://" + url

        # throw URLUnreachable exception for just incase
        try:
            res = requests.get(url)
        except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
            raise URLUnreachable("The URL is unreachable.")

        if res.status_code == 404:
            raise URLNotFound("The web page does not exists.")

        # its safe to assign the url and config
        self.url = url
        self.config = config


class GenericPreview(PreviewBase):
    """
    Extracts title, desc, img from a webpage's body instead of the meta tags.
    """
    pass
