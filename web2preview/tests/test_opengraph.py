from web2preview import *
from .test_fixtures import *


def test_extracts_n_assigns_properties_to_instance(open_graph_available):
    """
    OpenGraph extracts properties from a web page and assigns corresponding property-value to its instance.
    """
    ogpreview = OpenGraph(
        url="http://localhost:8000/open-graph/available.html",
        properties=["og:title", "og:price:amount"],
        content=open_graph_available,
    )
    assert ogpreview.title == "a title"
    assert ogpreview.price_amount == "1"


def test_unavailable_empty_properties_get_none(open_graph_unavailable):
    """
    OpenGraph assigns None to properties not found in the web page.
    """
    ogpreview = OpenGraph(
        url="http://localhost:8000/open-graph/unavailable.html",
        properties=["og:title", "og:price:amount"],
        content=open_graph_unavailable,
    )
    assert ogpreview.title is None
    assert "price_amount" not in ogpreview
