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
