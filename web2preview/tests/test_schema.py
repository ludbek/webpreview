def test_extracts_n_assigns_properties_to_instance(self):
    """
    Schema extracts properties from a web page and assigns corresponding property-value to its instance.
    """
    s = Schema("http://localhost:8000/schema/available.html", ["name", "camelCase"])
    self.assertEqual(s.name, "a title")
    self.assertEqual(s.camel_case, "camelCase changed to camel_case.")


def test_unavailable_empty_properties_get_none(self):
    """
    Schema assigns None to properties not found in the web page.
    """
    s = Schema("http://localhost:8000/schema/unavailable.html", ["name", "description"])
    self.assertEqual(s.name, None)
    self.assertEqual(s.description, None)
