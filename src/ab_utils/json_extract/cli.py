import argparse
import json
from pathlib import Path

from ab_utils.gemini.api import fetch_gemini
from ab_utils.gemini.models import GeminiOptions, ResponseMimeType
from ab_utils.gemini.constants import DEFAULT_GEMINI_MODEL

from .models import Invoice
from .constants import APP_NAME, JSON_EXTRACT_PROMPT


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(APP_NAME, help="Extract JSON from an image",
                                                            description="Extract JSON data from an image.")
    parser.add_argument("files", nargs="+",
                        type=Path, help="Path to one or more files")
    parser.add_argument("-t", "--type", default=None,
                        help="Type of input image (ex: 'invoice')")
    parser.add_argument("-p", "--prompt", default=JSON_EXTRACT_PROMPT,
                        help=f"ICS extraction prompt (default: {JSON_EXTRACT_PROMPT})")
    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("-o", "--output", default=None,
                        help="Output JSON file")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    response_schema = None
    if args.type == "invoice":
        response_schema = Invoice

    response = fetch_gemini(args.prompt, GeminiOptions(
        model=args.model,
        files=args.files or [],
        response_mime_type=(ResponseMimeType.JSON),
        response_schema=response_schema
    ))

    output = json.dumps(json.loads(response.text or "{}"), indent=2)

    if args.output:
        output_file = Path(args.output)
        output_file.write_text(output)
        print(f"Output written to {output_file.name}")
    else:
        print(output)
