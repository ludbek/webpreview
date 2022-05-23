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

    preview = web2preview(
        url=args.url,
        timeout=args.timeout,
        absolute_url=args.absolute_url,
    )

    print(
        (
            f"title: {preview.title}\n"
            f"description: {preview.description}\n"
            f"image: {preview.image}"
        )
    )
