import pytest


def foo(path: str) -> str:
    return ""


@pytest.fixture(scope="session")
def generic_preview_empty():
    foo("generic-preview/empty")
