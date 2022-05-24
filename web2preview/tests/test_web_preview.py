from urllib.parse import urlparse

from web2preview import *
from .test_fixtures import *


def test_extracts_title_via_open_graph(open_graph_available):
    """ """
    title, description, image = web_preview(
        "http://localhost:8000/open-graph/available.html", content=open_graph_available
    )
    assert title == "a title"


def test_extracts_title_via_twitter_card(twitter_card_available):
    """ """
    title, description, image = web_preview(
        "http://localhost:8000/twitter-card/available.html", content=twitter_card_available
    )
    assert title == "a title"


def test_extracts_title_via_schema(schema_available):
    """ """
    title, description, image = web_preview(
        "http://localhost:8000/schema/available.html", content=schema_available
    )
    assert title == "a title"


def test_extracts_description_via_generic_preview(generic_preview_h1_p_desc):
    """ """
    title, description, image = web_preview(
        "http://localhost:8000/generic-preview/h1-p-desc.html", content=generic_preview_h1_p_desc
    )
    assert description == "This is valid description."


def test_relative_image_path_returns_absolute_path_via_open_graph(
    open_graph_available_img_relative_path,
):
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/open-graph/available-img-relative-path.html"
    title, description, image = web_preview(
        url, absolute_image_url=True, content=open_graph_available_img_relative_path
    )
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)


def test_relative_image_path_returns_absolute_path_via_twitter_card(
    twitter_card_available_img_relative_path,
):
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/twitter-card/available-img-relative-path.html"
    title, description, image = web_preview(
        url, absolute_image_url=True, content=twitter_card_available_img_relative_path
    )
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)


def test_relative_image_path_returns_absolute_path_via_schema(schema_available_img_relative_path):
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/schema/available-img-relative-path.html"
    title, description, image = web_preview(
        url, absolute_image_url=True, content=schema_available_img_relative_path
    )
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)


def test_relative_image_path_returns_absolute_path_via_generic_preview(
    generic_preview_h1_img_relative_path,
):
    """
    When a relative image path is found, the full absolute path is returned if the flag is True.
    """
    url = "http://localhost:8000/generic-preview/h1-img-relative-path.html"
    title, description, image = web_preview(
        url, absolute_image_url=True, content=generic_preview_h1_img_relative_path
    )
    scheme, netloc, path, params, query, fragment = urlparse(url)
    base_url = "{}://{}".format(scheme, netloc)
    assert image.startswith(base_url)
