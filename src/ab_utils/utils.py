import io
import csv
from pathlib import Path
from PIL import Image


def compress_images_in_temp_dir(image_paths: list[Path], temp_dir: Path):
    output_paths: list[Path] = []

    for image_path in image_paths:
        print(f"Compressing {image_path.name}...")
        image = Image.open(image_path)
        image.thumbnail((1600, 1600))
        output_path = temp_dir / f"{image_path.stem}.jpg"
        image.convert("RGB").save(
            output_path, "JPEG", quality=80, optimize=True)
        output_paths.append(output_path)

    return output_paths


def flatten_dict(data: dict, parent_key: str = "") -> dict:
    result = {}

    for key, value in data.items():
        full_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            result.update(flatten_dict(value, full_key))
        elif not isinstance(value, list):
            result[full_key] = value

    return result


def json_to_csv(data: dict | list[dict]) -> str:
    if isinstance(data, list):
        records = data
    else:
        records = [data]

    output = io.StringIO(newline="")
    writer = None

    for record in records:
        # Find lists of dictionaries, such as line_items
        list_fields = {
            key: value
            for key, value in record.items()
            if isinstance(value, list)
            and value
            and isinstance(value[0], dict)
        }

        parent = {
            key: value
            for key, value in record.items()
            if key not in list_fields
        }
        parent_flat = flatten_dict(parent)

        if list_fields:
            # Expand each list into individual CSV rows
            list_key, items = next(iter(list_fields.items()))
            rows = [
                {**parent_flat, **flatten_dict(item, list_key)}for item in items]
        else:
            rows = [parent_flat]

        for row in rows:
            if writer is None:
                writer = csv.DictWriter(output, fieldnames=list(row.keys()))
                writer.writeheader()

            writer.writerow(row)

    return output.getvalue()
