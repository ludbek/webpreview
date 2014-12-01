from bs4 import BeautifulSoup
import requests
from requests.exceptions import *
import re
from bs4 import BeautifulSoup

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
        self._soup = BeautifulSoup(res.text)


class GenericPreview(PreviewBase):
    """
    Extracts title, desc, img from a webpage's body instead of the meta tags.
    """
    def __init__(self, *args):
        super(GenericPreview, self).__init__(*args)
        self.title = self._get_title()
        self.desc = self._get_desc()
        self.img = self._get_img()

    def _get_title(self):
        """
        Extract title from the given web page.
        """
        soup = self._soup
        # if title tag is present and has text in it, return it as the title
        if (soup.title and soup.title.text != ""):
            return soup.title.text
        # else if h1 tag is present and has text in it, return it as the title
        if (soup.h1 and soup.h1.text != ""):
            return soup.h1.text
        # if no title, h1 return None
        return None

    def _get_desc(self):
        """
        Extract desc from the given web page.
        """
        soup = self._soup
        # extract content preview from meta[name='description']
        meta_desc = soup.find('meta',attrs = {"name" : "description"})
        if(meta_desc and meta_desc['content'] !=""):
            return meta_desc['content']
        # else extract preview from the first <p> sibling to the first <h1>
        first_h1 = soup.find('h1')
        if first_h1:
            first_p = first_h1.find_next_sibling('p')
            if (first_p and first_p.string != ''):
                return first_p.string
        # else extract preview from the first <p>
        first_p = soup.find('p')
        if (first_p and first_p.string != ""):
            return first_p.string
        # else
        return None

    def _get_img(self):
        return None
