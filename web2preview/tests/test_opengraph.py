from web2preview import *


def test_extracts_n_assigns_properties_to_instance():
    """
    OpenGraph extracts properties from a web page and assigns corresponding property-value to its instance.
    """
    ogpreview = OpenGraph(
        url="http://localhost:8000/open-graph/available.html",
        properties=["og:title", "og:price:amount"],
    )
    assert ogpreview.title == "a title"
    assert ogpreview.price_amount == "1"


def test_unavailable_empty_properties_get_none():
    """
    OpenGraph assigns None to properties not found in the web page.
    """
    ogpreview = OpenGraph(
        url="http://localhost:8000/open-graph/unavailable.html",
        properties=["og:title", "og:price:amount"],
    )
    assert ogpreview.title is None
    assert ogpreview.price_amount is None
