def test_extracts_n_assigns_properties_to_instance(self):
    """
    TwitterCard extracts properties from a web page and assigns corresponding property-value to its instance.
    """
    tc = TwitterCard(
        "http://localhost:8000/twitter-card/available.html",
        ["twitter:title", "twitter:description"],
    )
    self.assertEqual(tc.title, "a title")
    self.assertEqual(tc.description, "a description")


def test_unavailable_empty_properties_get_none(self):
    """
    TwitterCard assigns None to properties not found in the web page.
    """
    tc = TwitterCard(
        "http://localhost:8000/twitter-card/unavailable.html",
        ["twitter:title", "twitter:description"],
    )
    self.assertEqual(tc.title, None)
    self.assertEqual(tc.description, None)
