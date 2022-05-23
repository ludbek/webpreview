from urllib.parse import urlparse

from web2preview import *


def test_extracts_title_via_open_graph():
    """ """
    title, description, image = web_preview("http://localhost:8000/open-graph/available.html")
    assert title == "a title"


def test_extracts_title_via_twitter_card():
    """ """
    title, description, image = web_preview("http://localhost:8000/twitter-card/available.html")
    assert title == "a title"


def test_extracts_title_via_schema():
    """ """
    title, description, image = web_preview("http://localhost:8000/schema/available.html")
    assert title == "a title"


def test_extracts_description_via_generic_preview():
    """ """
    title, description, image = web_preview("http://localhost:8000/generic-preview/h1-p-desc.html")
    assert description == "This is valid description."


def test_relative_image_path_returns_absolute_path_via_open_graph():
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/open-graph/available-img-relative-path.html"
    title, description, image = web_preview(url, absolute_image_url=True)
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)


def test_relative_image_path_returns_absolute_path_via_twitter_card():
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/twitter-card/available-img-relative-path.html"
    title, description, image = web_preview(url, absolute_image_url=True)
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)


def test_relative_image_path_returns_absolute_path_via_schema():
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/schema/available-img-relative-path.html"
    title, description, image = web_preview(url, absolute_image_url=True)
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)


def test_relative_image_path_returns_absolute_path_via_generic_preview():
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/generic-preview/h1-img-relative-path.html"
    title, description, image = web_preview(url, absolute_image_url=True)
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)
