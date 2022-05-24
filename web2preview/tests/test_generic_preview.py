from web2preview import *
from .test_fixtures import *


def test_default_properties_works(generic_preview_empty):
    """
    GenericPreview: Test if no properties list is passed the default properties is added.
    """
    apreview = GenericPreview("http://localhost:8000/", content=generic_preview_empty)
    assert apreview.properties == ["title", "description", "image"]


def test_extracts_title_from_title_tag(generic_preview_title):
    """
    GenericPreview: Test GenericPreview returns title from title tag if present.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/title.html", content=generic_preview_title
    )
    assert apreview.title == "This title is at the title tag."


def test_extracts_title_from_h1_tag(generic_preview_h1_title):
    """
    GenericPreview: Test GenericPreview returns title from the first <h1> tag if <title> is not present.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/h1-title.html", content=generic_preview_h1_title
    )
    assert apreview.title == "This title is from the first h1 tag."


def test_extracts_description_from_meta_tag(generic_preview_meta_desc):
    """
    GenericPreview: Test description is extracted from meta[name='description'] tag if present.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/meta-desc.html", content=generic_preview_meta_desc
    )
    assert apreview.description == "This description is from the meta[name='description']."


def test_extracts_description_from_the_first_h1_p(generic_preview_h1_p_desc):
    """
    GenericPreview: Test description is extracted from the first p sibling to the first h1.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/h1-p-desc.html", content=generic_preview_h1_p_desc
    )
    assert apreview.description == "This is valid description."


def test_extracts_description_from_the_first_p(generic_preview_p_desc):
    """
    GenericPreview: Test description is extracted from the first <p>.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/p-desc.html", content=generic_preview_p_desc
    )
    assert apreview.description == "This description is from the first p."


def test_extracts_image(generic_preview_h1_img):
    """
    GenericPreview: Test if url of image is returned if found in article body.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/h1-img.html", content=generic_preview_h1_img
    )
    assert apreview.image == "http://localhost:8000/img/heck.jpg"


def test_title_description_image_are_none_if_none_found(generic_preview_empty):
    """
    GenericPreview: Test if title, description and image could not be found all are assigned None.
    """
    apreview = GenericPreview(
        "http://localhost:8000/generic-preview/empty.html", content=generic_preview_empty
    )
    assert apreview.title is None
    assert apreview.description is None
    assert apreview.image is None
