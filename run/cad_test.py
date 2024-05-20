from collections import defaultdict
import csv
import hashlib
import requests
from pathlib import Path
from uuid import uuid4

from PIL import Image


def post_file(group_id, directory, filename, md5):
    requests.post(
        url="http://127.0.0.1:5000/api/file",
        json={
            "group_id": group_id,
            "directory": directory,
            "filename": filename,
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


def parse_logfile(logfile) -> defaultdict[Path, list[str]]:
    file2renders = defaultdict(list)
    with open(logfile) as f:
        for i, (file_abspath, render_abspath) in enumerate(csv.reader(f)):
            if i == 0:
                continue
            file2renders[Path(file_abspath)].append(render_abspath)
    return file2renders


parent_renders_dir = Path("C:/Users/ryanh/Documents/cad/data/renders")
parent_data_dir = Path("C:/Users/ryanh/Documents/cad/data")

for render_dir in parent_renders_dir.glob("*"):
    group_id = str(uuid4())
    logfile = next(render_dir.glob("CadConversion*"))
    file2renders = parse_logfile(logfile)
    cad_dir = Path(next(iter(file2renders))).parent
    for cad_path in cad_dir.glob("*"):
        with open(cad_path, "rb") as f:
            file_bytes = f.read()
        file_md5 = hashlib.md5(file_bytes).hexdigest()
        file_relpath = Path(cad_path).relative_to(parent_data_dir)
        post_file(
            group_id=group_id,
            directory=str(file_relpath.parent),
            filename=file_relpath.name,
            md5=file_md5,
        )
        post_file_data(
            md5=file_md5, num_bytes=len(file_bytes), local_path=str(cad_path)
        )
        for i, render_abspath in enumerate(file2renders[cad_path]):
            post_image(md5=file_md5, order=i, path=render_abspath)
            if not render_abspath.endswith(("iso.png", "front.png", "right.png")):
                continue
            image = Image.open(render_abspath)
            image.thumbnail((80, 80))
            thumbnail_path = render_abspath.removesuffix(".png") + "_thumbnail.png"
            image.save(thumbnail_path)
            post_thumbnail(md5=file_md5, order=i, path=thumbnail_path)
