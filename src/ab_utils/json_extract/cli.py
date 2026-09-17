import argparse
import json
from tempfile import TemporaryDirectory
from pathlib import Path
from google import genai

from ab_utils.gemini_client import client as gemini_client
from ab_utils.utils import compress_images_in_temp_dir
from ab_utils.constants import JSON_EXTRACT_APP_NAME, DEFAULT_GEMINI_MODEL

from .constants import INVOICE_JSON_EXTRACT_PROMPT, JSON_EXTRACT_PROMPT


def extract_json_from_images(file_paths: list[Path], prompt: str, model: str):
    """Extract JSON from images"""

    print(
        f"Extracting JSON data from: {', '.join([file.name for file in file_paths])}")

    files: list[genai.types.File] = []
    for file_path in file_paths:
        file = gemini_client.files.upload(file=file_path)
        files.append(file)
        print(f"Uploaded {file_path.name}")

    chat = gemini_client.chats.create(
        model=model,
        config=genai.types.GenerateContentConfig(response_mime_type="application/json"))
    response = chat.send_message([*files, prompt])
    result = json.loads(response.text or "{}")

    return result


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(JSON_EXTRACT_APP_NAME, help="Extract JSON from an image",
                                                            description="Extract JSON data from an image.")
    parser.add_argument("images", nargs="+",
                        help="Path to one or more image files")
    parser.add_argument("-m", "--model", default=DEFAULT_GEMINI_MODEL,
                        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("-p", "--prompt", default=None,
                        help=f"JSON extraction prompt (default: {JSON_EXTRACT_PROMPT})")
    parser.add_argument("-t", "--type", default=None,
                        help="Type of input image (ex: 'invoice')")
    parser.add_argument("-o", "--output", default=None,
                        help="Output JSON file")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    input_image_paths: list[Path] = []
    for image in args.images:
        input_image_paths.append(Path(image))

    output_json_path = Path(args.output) if args.output else None

    with TemporaryDirectory() as temp_dir:
        compressed_image_paths = compress_images_in_temp_dir(
            input_image_paths, temp_dir=Path(temp_dir))

        prompt = JSON_EXTRACT_PROMPT
        if not args.prompt:
            if args.type == "invoice":
                prompt = INVOICE_JSON_EXTRACT_PROMPT

        result = extract_json_from_images(
            compressed_image_paths, prompt, args.model)

        if (output_json_path):
            with open(output_json_path, "w") as f:
                json.dump(result, f, indent=2)
                print(f'Extracted JSON written to: {output_json_path.name}')
        else:
            print("Extracted JSON:\n", json.dumps(result, indent=2))
