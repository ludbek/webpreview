import unittest

from webpreview.previews import *
from webpreview.excepts import *

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
        apreview = PreviewBase(aurl, ["title"])
        self.assertEqual(apreview.url, aurl)

    def test_url_without_schema_gets_http_appended(self):
        """
        PreviewBase: Test if "http://" is added URL without schema.
        example.com to http://example.com
        """
        aurl2 = 'wikipedia.com'
        apreview2 = PreviewBase(aurl2, ['title'])
        self.assertEqual(apreview2.url, "http://" + aurl2)

    def test_properties_is_added_to_instance(self):

        """
        PreviewBase: Test if passed "properties" are added to the instance.
        """
        apreview = PreviewBase("http://localhost:8000/", ['title', 'author'])
        self.assertEqual(apreview.properties, ['title', 'author'])

    def test_dns_errors(self):
        """
        PreviewBase: Test if DNS errors can be caught.
        """
        try:
            PreviewBase("http://thisurldoesnotexists7352356.urlz", ['title'])
        except URLUnreachable as e:
            self.assertEqual(URLUnreachable, type(e))
            return
        self.fail("Should throw the DNS error.")

    def test_url_exists(self):
        """
        PreviewBase: Test if URL exists.
        """
        try:
            PreviewBase("http://localhost:8000/thisdoesnotexists7")
        except URLNotFound as e:
            self.assertEqual(URLNotFound, type(e))
            return
        self.fail("Should throw the 404 error.")

    def test_complains_about_empty_property_list(self):
        """
        PreviewBase complains about empty property list.
        """
        try:
            PreviewBase("http://localhost:8000")
            PreviewBase("http://localhost:8000", [])
        except EmptyProperties as e:
            self.assertEqual(EmptyProperties, type(e))
            return
        self.fail("Should should complain about empty property list.")


class TestGenericPreview(unittest.TestCase):
    """
    Test GenericPreview.
    """
    def test_default_properties_works(self):
        """
        GenericPreview: Test if no properties list is passed the default properties is added.
        """
        apreview = GenericPreview("http://localhost:8000/")
        self.assertEqual(apreview.properties, ['title', 'description', 'image'])

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

    def test_extracts_description_from_meta_tag(self):
        """
        GenericPreview: Test description is extracted from meta[name='description'] tag if present.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/meta-desc.html")
        self.assertEqual(apreview.description, "This description is from the meta[name='description'].")

    def test_extracts_description_from_the_first_h1_p(self):
        """
        GenericPreview: Test description is extracted from the first p sibling to the first h1.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/h1-p-desc.html")
        self.assertEqual(apreview.description, "This is valid description.")

    def test_extracts_description_from_the_first_p(self):
        """
        GenericPreview: Test description is extracted from the first <p>.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/p-desc.html")
        self.assertEqual(apreview.description, "This description is from the first p.")

    def test_extracts_image(self):
        """
        GenericPreview: Test if url of image is returned if found in article body.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/h1-img.html")
        self.assertEqual(apreview.image, "http://localhost:8000/img/heck.jpg")

    def test_title_description_image_are_none_if_none_found(self):
        """
        GenericPreview: Test if title, description and image could not be found all are assigned None.
        """
        apreview = GenericPreview("http://localhost:8000/generic-preview/empty.html")
        self.assertEqual(apreview.title, None)
        self.assertEqual(apreview.description, None)
        self.assertEqual(apreview.image, None)


class TestOpenGraph(unittest.TestCase):
    """
    Test OpenGraph.
    """
    def test_extracts_n_assigns_properties_to_instance(self):
        """
        OpenGraph extracts properties from a web page and assigns corresponding property-value to its instance.
        """
        ogpreview = OpenGraph("http://localhost:8000/open-graph/available.html", ['og:title', 'og:price:amount'])
        self.assertEqual(ogpreview.title, "a title")
        self.assertEqual(ogpreview.price_amount, "1")

    def test_unavailable_empty_properties_get_none(self):
        """
        OpenGraph assigns None to properties not found in the web page.
        """
        ogpreview = OpenGraph("http://localhost:8000/open-graph/unavailable.html", ['og:title', 'og:price:amount'])
        self.assertEqual(ogpreview.title, None)
        self.assertEqual(ogpreview.price_amount, None)



class TestTwitterCard(unittest.TestCase):
    """
    Test TwitterCard.
    """
    def test_extracts_n_assigns_properties_to_instance(self):
        """
        TwitterCard extracts properties from a web page and assigns corresponding property-value to its instance.
        """
        tc = TwitterCard("http://localhost:8000/twitter-card/available.html", ['twitter:title', 'twitter:description'])
        self.assertEqual(tc.title, "a title")
        self.assertEqual(tc.description, "a description")

    def test_unavailable_empty_properties_get_none(self):
        """
        TwitterCard assigns None to properties not found in the web page.
        """
        tc = TwitterCard("http://localhost:8000/twitter-card/unavailable.html", ['twitter:title', 'twitter:description'])
        self.assertEqual(tc.title, None)
        self.assertEqual(tc.description, None)


class TestSchema(unittest.TestCase):
    """
    Test Schema.
    """
    def test_extracts_n_assigns_properties_to_instance(self):
        """
        Schema extracts properties from a web page and assigns corresponding property-value to its instance.
        """
        s = Schema("http://localhost:8000/schema/available.html", ['name', 'camelCase'])
        self.assertEqual(s.name, "a title")
        self.assertEqual(s.camel_case, "camelCase changed to camel_case.")

    def test_unavailable_empty_properties_get_none(self):
        """
        Schema assigns None to properties not found in the web page.
        """
        s = Schema("http://localhost:8000/schema/unavailable.html", ['name', 'description'])
        self.assertEqual(s.name, None)
        self.assertEqual(s.description,  None)


class TestWebPreview(unittest.TestCase):
    """
    Test web_preview.
    """
    def test_extracts_title_via_openg_graph(self):
        """
        """
        title, description, image = web_preview("http://localhost:8000/open-graph/available.html")
        self.assertEqual(title, "a title")

    def test_extracts_title_via_twitter_card(self):
        """
        """
        title, description, image = web_preview("http://localhost:8000/twitter-card/available.html")
        self.assertEqual(title, "a title")

    def test_extracts_title_via_schema(self):
        """
        """
        title, description, image = web_preview("http://localhost:8000/schema/available.html")
        self.assertEqual(title, "a title")

    def test_extracts_description_via_generic_preview(self):
        """
        """
        title, description, image = web_preview("http://localhost:8000/generic-preview/h1-p-desc.html")
        self.assertEqual(description, "This is valid description.")


if __name__ == '__main__':
    unittest.main()
