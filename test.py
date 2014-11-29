import unittest
from webpreview import PreviewBase
from webpreview import EmptyURL, InvalidURL

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

    def test_catches_invalid_url(self):
        """
        PreviewBase: Test it catches invalid urls
        """
        try:
            PreviewBase('invalidurl')
        except InvalidURL as e:
            self.assertEqual(InvalidURL, type(e))

        try:
            PreviewBase('ascheme://invalidurl.com')
        except InvalidURL as e:
            self.assertEqual(InvalidURL, type(e))

    def test_instance_gets_valid_url(self):
        """
        PreviewBase: Test instance gets the valid url being passed.
        """
        aurl = "validurl.com"
        apreview = PreviewBase(aurl)
        self.assertEqual(apreview.url, aurl)

    def test_allows_url_without_scheme(self):
        """
        PreviewBase: Test it allows urls without scheme.
        e.g: example.com, www.example.com
        """
        aurl = 'validurl.com'
        apreview = PreviewBase(aurl)
        self.assertEqual(apreview.url, aurl)

        aurl2 = 'www.validurl.com'
        apreview2 = PreviewBase(aurl2)
        self.assertEqual(apreview2.url, aurl2)

    def test_default_config_works(self):
        """
        PreviewBase: Test if no config list is passed the default config is added.
        """
        apreview = PreviewBase("avalidurl.com")
        self.assertEqual(apreview.config, ['title', 'desc', 'img'])

    def test_config_is_added_to_instance(self):

        """
        PreviewBase: Test if config list is past, its added to the instance.
        """
        apreview = PreviewBase("avalidurl.com", ['title', 'author'])
        self.assertEqual(apreview.config, ['title', 'author'])

if __name__ == '__main__':
    unittest.main()
