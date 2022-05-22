from argparse import ArgumentParser

from .excepts import *
from .previews import *


def main() -> None:
    parser = ArgumentParser("web2preview")
    parser.add_argument("url", type=str, help="URL to parse")
    parser.add_argument(
        "--timeout", "-t", type=int, help="Timeout in seconds when requestion URL", default=30
    )
    parser.add_argument(
        "--absolute-url", "-a", help="Convert returned urls to absolute", action="store_true"
    )
    args = parser.parse_args()

    title, description, image = web2preview(
        url=args.url,
        timeout=args.timeout,
        absolute_image_url=args.absolute_url,
    )

    print((f"title: {title}\n" f"description: {description}\n" f"image: {image}"))
