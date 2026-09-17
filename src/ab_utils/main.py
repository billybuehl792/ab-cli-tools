import argparse
from pillow_heif.as_plugin import register_heif_opener

from .ics_extract.cli import add_parser as calendar_event_extractor_parser
from .json_extract.cli import add_parser as image_json_extractor_parser
from .photosheet.cli import add_parser as photosheet_parser
from .constants import COMPANY_NAME

register_heif_opener()


def main():
    parser = argparse.ArgumentParser(
        prog="ab_utils", description=f"{COMPANY_NAME} tools")

    subparsers = parser.add_subparsers(dest="command", required=True)

    calendar_event_extractor_parser(subparsers)
    image_json_extractor_parser(subparsers)
    photosheet_parser(subparsers)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
