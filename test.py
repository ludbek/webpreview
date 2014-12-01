import unittest
from webpreview import PreviewBase
from webpreview import EmptyURL, InvalidURL, URLNotFound, URLUnreachable

class TestPreviewBase(unittest.TestCase):
    """
    Test PreviewBase.
    """
    def test_it_complains_url_absence(self):
        """
        PreviewBase: Test it complains absence of url for preview.
        """
        try:
            PreviewBase()
        except EmptyURL as e:
            self.assertEqual(type(e), EmptyURL)
            return
        self.fail("Should complain about the empty URL.")

    def test_instance_gets_valid_url(self):
        """
        PreviewBase: Test instance gets the valid url being passed.
        """
        aurl = "http://validurl.com"
        apreview = PreviewBase(aurl)
        self.assertEqual(apreview.url, aurl)

    def test_url_without_schema_gets_http_appended(self):
        """
        PreviewBase: Test if "http://" is added URL without schema.
        example.com to http://example.com
        """
        aurl2 = 'wikipedia.com'
        apreview2 = PreviewBase(aurl2)
        self.assertEqual(apreview2.url, "http://" + aurl2)

    def test_default_config_works(self):
        """
        PreviewBase: Test if no config list is passed the default config is added.
        """
        apreview = PreviewBase("www.wikipedia.com")
        self.assertEqual(apreview.config, ['title', 'desc', 'img'])

    def test_config_is_added_to_instance(self):

        """
        PreviewBase: Test if config list is past, its added to the instance.
        """
        apreview = PreviewBase("wikipedia.com", ['title', 'author'])
        self.assertEqual(apreview.config, ['title', 'author'])

    def test_dns_errors(self):
        """
        PreviewBase: Test if DNS errors can be caught.
        """
        try:
            PreviewBase("http://thisurldoesnotexists7352356.urlz")
        except URLUnreachable as e:
            self.assertEqual(URLUnreachable, type(e))
            return
        self.fail("Should throw the DNS error.")

    def test_url_exists(self):
        """
        PreviewBase: Test if URL exists.
        """
        try:
            PreviewBase("http://en.wikipedia.org/wiki/thisdoesnotexists7")
        except URLNotFound as e:
            self.assertEqual(URLNotFound, type(e))
            return
        self.fail("Should throw the 404 error.")

if __name__ == '__main__':
    unittest.main()
