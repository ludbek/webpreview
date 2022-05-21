from web2preview import *


def test_default_properties_works():
    """
    GenericPreview: Test if no properties list is passed the default properties is added.
    """
    apreview = GenericPreview("http://localhost:8000/")
    assert apreview.properties == ["title", "description", "image"]


def test_extracts_title_from_title_tag():
    """
    GenericPreview: Test GenericPreview returns title from title tag if present.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/title.html")
    assert apreview.title == "This title is at the title tag."


def test_extracts_title_from_h1_tag():
    """
    GenericPreview: Test GenericPreview returns title from the first <h1> tag if <title> is not present.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/h1-title.html")
    assert apreview.title == "This title is from the first h1 tag."


def test_extracts_description_from_meta_tag():
    """
    GenericPreview: Test description is extracted from meta[name='description'] tag if present.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/meta-desc.html")
    assert apreview.description == "This description is from the meta[name='description']."


def test_extracts_description_from_the_first_h1_p():
    """
    GenericPreview: Test description is extracted from the first p sibling to the first h1.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/h1-p-desc.html")
    assert apreview.description == "This is valid description."


def test_extracts_description_from_the_first_p():
    """
    GenericPreview: Test description is extracted from the first <p>.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/p-desc.html")
    assert apreview.description == "This description is from the first p."


def test_extracts_image():
    """
    GenericPreview: Test if url of image is returned if found in article body.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/h1-img.html")
    assert apreview.image == "http://localhost:8000/img/heck.jpg"


def test_title_description_image_are_none_if_none_found():
    """
    GenericPreview: Test if title, description and image could not be found all are assigned None.
    """
    apreview = GenericPreview("http://localhost:8000/generic-preview/empty.html")
    assert apreview.title is None
    assert apreview.description is None
    assert apreview.image is None
