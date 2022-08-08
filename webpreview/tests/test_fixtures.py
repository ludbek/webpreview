import pytest


def get_contents(path: str) -> str:
    with open(path) as f:
        contents = f.read()
    return contents


@pytest.fixture(scope="session")
def generic_preview_empty() -> str:
    return get_contents("tests/generic-preview/empty.html")


@pytest.fixture(scope="session")
def generic_preview_h1_img_relative_path() -> str:
    return get_contents("tests/generic-preview/h1-img-relative-path.html")


@pytest.fixture(scope="session")
def generic_preview_h1_img() -> str:
    return get_contents("tests/generic-preview/h1-img.html")


@pytest.fixture(scope="session")
def generic_preview_h1_p_desc() -> str:
    return get_contents("tests/generic-preview/h1-p-desc.html")


@pytest.fixture(scope="session")
def generic_preview_h1_title() -> str:
    return get_contents("tests/generic-preview/h1-title.html")


@pytest.fixture(scope="session")
def generic_preview_meta_desc() -> str:
    return get_contents("tests/generic-preview/meta-desc.html")


@pytest.fixture(scope="session")
def generic_preview_p_desc() -> str:
    return get_contents("tests/generic-preview/p-desc.html")


@pytest.fixture(scope="session")
def generic_preview_title() -> str:
    return get_contents("tests/generic-preview/title.html")


@pytest.fixture(scope="session")
def open_graph_available_img_relative_path() -> str:
    return get_contents("tests/open-graph/available-img-relative-path.html")


@pytest.fixture(scope="session")
def open_graph_available() -> str:
    return get_contents("tests/open-graph/available.html")


@pytest.fixture(scope="session")
def open_graph_unavailable() -> str:
    return get_contents("tests/open-graph/unavailable.html")


@pytest.fixture(scope="session")
def schema_available_img_relative_path() -> str:
    return get_contents("tests/schema/available-img-relative-path.html")


@pytest.fixture(scope="session")
def schema_available() -> str:
    return get_contents("tests/schema/available.html")


@pytest.fixture(scope="session")
def schema_unavailable() -> str:
    return get_contents("tests/schema/unavailable.html")


@pytest.fixture(scope="session")
def twitter_card_available_img_relative_path() -> str:
    return get_contents("tests/twitter-card/available-img-relative-path.html")


@pytest.fixture(scope="session")
def twitter_card_available() -> str:
    return get_contents("tests/twitter-card/available.html")


@pytest.fixture(scope="session")
def twitter_card_unavailable() -> str:
    return get_contents("tests/twitter-card/unavailable.html")
