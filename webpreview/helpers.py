"""Helpers module.

Compatibility layer with original webpreview library.
"""

from typing import Optional

from .parsers import make_absolute_url


def process_image_url(
    request_url: Optional[str] = None,
    image_url: Optional[str] = None,
    force_absolute_url: bool = True,
) -> Optional[str]:
    if not force_absolute_url:
        return image_url

    return make_absolute_url(image_url, request_url)
