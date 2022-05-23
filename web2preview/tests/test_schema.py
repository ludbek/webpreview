from web2preview import *


def test_extracts_n_assigns_properties_to_instance():
    """
    Schema extracts properties from a web page and assigns corresponding property-value to its instance.
    """
    s = Schema("http://localhost:8000/schema/available.html", ["name", "camelCase"])
    assert s.name == "a title"
    assert s.camel_case == "camelCase changed to camel_case."


def test_unavailable_empty_properties_get_none():
    """
    Schema assigns None to properties not found in the web page.
    """
    s = Schema("http://localhost:8000/schema/unavailable.html", ["name", "description"])
    assert "name" not in s
    assert s.description is None
