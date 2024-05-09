from pathlib import Path
import random

import numpy as np
from PIL import Image
import requests
from string import ascii_lowercase

hex_lowercase = "0123456789abcdef"


def random_gradient(width: int, height: int):
    image = Image.new("RGB", (width, height))
    start_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
    end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    data = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(width):
        # Calculate the interpolation factor
        ratio = i / width
        # Interpolate between start and end colors
        intermediate_color = [
            int(start_color[j] * (1 - ratio) + end_color[j] * ratio) for j in range(3)
        ]
        data[:, i] = intermediate_color

    image = Image.fromarray(data)
    return image


def post_file(group_id, file_path, md5):
    requests.post(
        url="http://127.0.0.1:5000/api/file",
        json={
            "group_id": group_id,
            "file_path": file_path,
            "md5": md5,
        },
    )


def post_file_data(md5, num_bytes, local_path):
    requests.post(
        url="http://127.0.0.1:5000/api/file-data",
        json={"md5": md5, "num_bytes": num_bytes, "local_path": local_path},
    )


def post_image(md5, order, path):
    requests.post(
        url="http://127.0.0.1:5000/api/image",
        json={"md5": md5, "order": order, "path": path},
    )


def post_thumbnail(md5, order, path):
    requests.post(
        url="http://127.0.0.1:5000/api/thumbnail",
        json={"md5": md5, "order": order, "path": path},
    )


group_ids = ["group-1", "group-2", "group-3"]
rootdir = Path("files").absolute()
rootdir.mkdir()
for group_id in group_ids:
    group_dir = rootdir / group_id
    group_dir.mkdir()
    num_files_per_group = random.randint(4, 8)
    for _ in range(num_files_per_group):
        file_md5 = "".join(random.choices(hex_lowercase, k=32))
        filename = "".join(random.choices(ascii_lowercase, k=10)) + ".ext"
        post_file(group_id, f"rel/path/{filename}", file_md5)
        post_file_data(file_md5, random.randint(10**3, 10**8), "")
        num_images_per_file = random.randint(1, 4)
        for order in range(num_images_per_file):
            width = random.randint(300, 1000)
            height = random.randint(300, 1000)
            img = random_gradient(width, height)
            img_path = group_dir / f"{file_md5}-{order}.png"
            img.save(img_path)
            post_image(file_md5, order, str(img_path))
            img.thumbnail((80, 80))
            thumbnail_path = group_dir / f"{file_md5}-{order}-thumbnail.png"
            img.save(thumbnail_path)
            post_thumbnail(file_md5, order, str(thumbnail_path))
