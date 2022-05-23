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
    aurl = "http://localhost:8000/"
    apreview = PreviewBase(aurl, properties=["title"], timeout=1)
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
    assert apreview.properties == ["title", "author"]


def test_dns_errors():
    """
    PreviewBase: Test if DNS errors can be caught.
    """
    with pytest.raises(URLUnreachable):
        PreviewBase("http://thisurldoesnotexists7352356.urlz", ["title"], timeout=1)


def test_url_exists():
    """
    PreviewBase: Test if URL exists.
    """
    with pytest.raises(URLNotFound):
        PreviewBase("http://localhost:8000/thisdoesnotexists7", timeout=1)


def test_complains_about_empty_property_list():
    """
    PreviewBase complains about empty property list.
    """
    with pytest.raises(EmptyProperties):
        PreviewBase("http://localhost:8000")
        PreviewBase("http://localhost:8000", [])
