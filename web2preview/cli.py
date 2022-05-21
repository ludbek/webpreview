from argparse import ArgumentParser

from .exceptions import *
from .previews import *


def main() -> None:
    parser = ArgumentParser("web2preview")
    parser.add_argument("url", type=str, help="URL to parse")
    parser.add_argument("--timeout", "-t", type=int, help="Timeout in seconds when requestion URL", default=30)
    parser.add_argument("--absolute-image-url", "-a", help="Convert image url to absolute URL", action="store_true")
    args = parser.parse_args()

    title, description, image = web_preview(
        url=args.url,
        timeout=args.timeout,
        absolute_image_url=args.absolute_image_url,
    )

    print((
        f"url: {args.url}\n"
        f"title: {title}\n"
        f"description: {description}\n"
        f"image: {image}"
    ))
