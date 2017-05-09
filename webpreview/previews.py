import re

import requests
from requests.exceptions import *
from bs4 import BeautifulSoup

from .excepts import *


class PreviewBase(object):
    """
    Base for all web preview.
    """
    def __init__(self, url = None, properties = None, timeout=None, headers=None):
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
            res = requests.get(url, timeout=timeout, headers=headers)
        except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
            raise URLUnreachable("The URL does not exists.")
        except MissingSchema: # if no schema add http as default
            url = "http://" + url

        # throw URLUnreachable exception for just incase
        try:
            res = requests.get(url, timeout=timeout, headers=headers)
        except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
            raise URLUnreachable("The URL is unreachable.")

        if res.status_code == 404:
            raise URLNotFound("The web page does not exists.")

        # its safe to assign the url
        self.url = url


        if not properties:
            raise EmptyProperties("Please pass list of properties to be extracted.")
        # its safe to assign properties
        self.properties = properties
        self._soup = BeautifulSoup(res.text, "html.parser")


class GenericPreview(PreviewBase):
    """
    Extracts title, description, image from a webpage's body instead of the meta tags.
    """
    def __init__(self, url = None, properties = ['title', 'description', 'image'], timeout=None, headers=None):
        super(GenericPreview, self).__init__(url, properties, timeout=timeout, headers=headers)
        self.title = self._get_title()
        self.description = self._get_description()
        self.image = self._get_image()

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

    def _get_description(self):
        """
        Extract description from the given web page.
        """
        soup = self._soup
        # extract content preview from meta[name='description']
        meta_description = soup.find('meta',attrs = {"name" : "description"})
        if(meta_description and meta_description['content'] !=""):
            return meta_description['content']
        # else extract preview from the first <p> sibling to the first <h1>
        first_h1 = soup.find('h1')
        if first_h1:
            first_p = first_h1.find_next('p')
            if (first_p and first_p.string != ''):
                return first_p.text
        # else extract preview from the first <p>
        first_p = soup.find('p')
        if (first_p and first_p.string != ""):
            return first_p.string
        # else
        return None

    def _get_image(self):
        """
        Extract preview image from the given web page.
        """
        soup = self._soup
        # extract the first image which is sibling to the first h1
        first_h1 = soup.find('h1')
        if first_h1:
            first_image = first_h1.find_next_sibling('img')
            if first_image and first_image['src'] != "":
                return first_image['src']
        return None


class SocialPreviewBase(PreviewBase):
    """
    Abstract class for OpenGraph, TwitterCard and Google+.
    """
    def __init__(self, *args, **kwargs):
        super(SocialPreviewBase, self).__init__(*args, **kwargs)
        self._set_properties()
        # OpengGraph has <meta property="" content="">
        # TwitterCard  has <meta name="" content="">
        # Google+  has <meta itemprop="" content="">
        # override this self._target_attribute

    def _set_properties(self):
        soup = self._soup
        for property in self.properties:
            property_meta = soup.find('meta', attrs = {self._target_attribute : property})
            # turn "og:title" to "title" and "og:price:amount" to price_amount
            if re.search(r":", property):
                new_property =  property.split(':',1)[1].replace(':', '_')
            # turn "camelCase" to "camel_case"
            elif re.search(r"[A-Z]", property):
                # regex taken from 2nd answer at http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
                new_property = re.sub('(?!^)([A-Z]+)', r'_\1',property).lower()
            else:
                new_property = property

            if property_meta and property_meta['content'] != "":
                # dynamically attach property to instance
                self.__dict__[new_property] = property_meta['content']
            else:
                self.__dict__[new_property] = None


class OpenGraph(SocialPreviewBase):
    """
    Gets OpenGraph meta properties of a webpage.
    """
    def __init__(self, *args, **kwargs):
        self._target_attribute =  "property"
        super(OpenGraph, self).__init__(*args, **kwargs)


class TwitterCard(SocialPreviewBase):
    """
    Gets TwitterCard meta properties of a webpage.
    """
    def __init__(self, *args, **kwargs):
        self._target_attribute =  "name"
        super(TwitterCard, self).__init__(*args, **kwargs)


class Schema(SocialPreviewBase):
    """
    Gets Schema meta properties from a website.
    """
    def __init__(self, *args, **kwargs):
        self._target_attribute =  "itemprop"
        super(Schema, self).__init__(*args, **kwargs)


def web_preview(url, timeout=None, headers=None):
    """
    Extract title, description and image from OpenGraph or TwitterCard or Schema or GenericPreview. Which ever returns first.
    """
    og = OpenGraph(url, ['og:title', 'og:description', 'og:image'], timeout=timeout, headers=headers)
    if og.title:
        return og.title, og.description, og.image

    tc = TwitterCard(url, ['twitter:title', 'twitter:description', 'twitter:image'], timeout=timeout, headers=headers)
    if tc.title:
        return tc.title, tc.description, tc.image

    s = Schema(url, ['name', 'description', 'image'], timeout=timeout, headers=headers)
    if s.name:
        return s.name, s.description, s.image

    gp = GenericPreview(url, timeout=timeout, headers=headers)
    return gp.title, gp.description, gp.image
