import unittest
from webpreview import PreviewBase, GenericPreview
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


class TestGenericPreview(unittest.TestCase):
    """
    Test GenericPreview.
    """
    def test_extracts_title_from_title_tag(self):
        """
        GenericPreview: Test GenericPreview returns title from title tag if present.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/title.html")
        self.assertEqual(apreview.title, "This title is at the title tag.")


    def test_extracts_title_from_h1_tag(self):
        """
        GenericPreview: Test GenericPreview returns title from the first <h1> tag if <title> is not present.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/h1-title.html")
        self.assertEqual(apreview.title, "This title is from the first h1 tag.")

    def test_extracts_desc_from_meta_tag(self):
        """
        GenericPreview: Test description is extracted from meta[name='description'] tag if present.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/meta-desc.html")
        self.assertEqual(apreview.desc, "This description is from the meta[name='description'].")

    def test_extracts_desc_from_the_first_h1_p(self):
        """
        GenericPreview: Test description is extracted from the first p sibling to the first h1.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/h1-p-desc.html")
        self.assertEqual(apreview.desc, "This description is from the first h1>p[0].")

    def test_extracts_desc_from_the_first_p(self):
        """
        GenericPreview: Test description is extracted from the first <p>.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/p-desc.html")
        self.assertEqual(apreview.desc, "This description is from the first p.")

    def test_extracts_img(self):
        """
        GenericPreview: Test if url of image is returned if found in article body.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/h1-img.html")
        self.assertEqual(apreview.img, "http://localhost:8000/img/heck.img")


if __name__ == '__main__':
    unittest.main()
