import pytest

from web2preview import *


def test_it_complains_url_absence():
    """
    PreviewBase: Test it complains absence of url for preview.
    """
    with pytest.raises(EmptyURL):
        PreviewBase()


def test_instance_gets_valid_url():
    """
    PreviewBase: Test instance gets the valid url being passed.
    """
    aurl = "http://validurl.com"
    apreview = PreviewBase(aurl, properties=["title"])
    assert apreview.url == aurl


def test_url_without_schema_gets_http_appended():
    """
    PreviewBase: Test if "http://" is added URL without schema.
    example.com to http://example.com
    """
    aurl2 = "wikipedia.com"
    apreview2 = PreviewBase(aurl2, properties=["title"])
    assert apreview2.url == "http://" + aurl2


def test_properties_is_added_to_instance():

    """
    PreviewBase: Test if passed "properties" are added to the instance.
    """
    apreview = PreviewBase("http://localhost:8000/", ["title", "author"])
    self.assertEqual(apreview.properties, ["title", "author"])


def test_dns_errors():
    """
    PreviewBase: Test if DNS errors can be caught.
    """
    try:
        PreviewBase("http://thisurldoesnotexists7352356.urlz", ["title"])
    except URLUnreachable as e:
        self.assertEqual(URLUnreachable, type(e))
        return
    self.fail("Should throw the DNS error.")


def test_url_exists():
    """
    PreviewBase: Test if URL exists.
    """
    try:
        PreviewBase("http://localhost:8000/thisdoesnotexists7")
    except URLNotFound as e:
        self.assertEqual(URLNotFound, type(e))
        return
    self.fail("Should throw the 404 error.")


def test_complains_about_empty_property_list(self):
    """
    PreviewBase complains about empty property list.
    """
    try:
        PreviewBase("http://localhost:8000")
        PreviewBase("http://localhost:8000", [])
    except EmptyProperties as e:
        self.assertEqual(EmptyProperties, type(e))
        return
    self.fail("Should should complain about empty property list.")
