import os
from pathlib import PurePosixPath

from flask import Blueprint, render_template, request

from .models import db, File, FileData, Thumbnail


view_blueprint = Blueprint("view", __name__)


from flask import send_from_directory, abort


def convert_size(size: int):
    size = float(size)
    suffixes = ["B", "KB", "MB", "GB"]
    suffix_idx = 0
    while size >= 1024 and suffix_idx < 3:
        size /= 1024
        suffix_idx += 1
    return f"{round(size)} {suffixes[suffix_idx]}"


@view_blueprint.route("/thumbnail/<path:filepath>")
def serve_thumbnail(filepath: str):
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    try:
        return send_from_directory(directory, filename)
    except FileNotFoundError:
        abort(404)


@view_blueprint.route("/", methods=["GET"])
def index() -> str:
    filename_filter = request.args.get("filename", "").strip()
    extension_filter = request.args.get("extension", "").strip().lower()

    data_query = (
        db.session.query(
            File.group_id,
            File.file_path,
            FileData.num_bytes,
            Thumbnail.path,
            Thumbnail.order,
        )
        .outerjoin(FileData, File.md5 == FileData.md5)
        .outerjoin(Thumbnail, File.md5 == Thumbnail.md5)
    )

    if filename_filter:
        data_query = data_query.filter(File.file_path.ilike(f"%{filename_filter}%"))
    if extension_filter:
        data_query = data_query.filter(File.file_path.ilike(f"%{extension_filter}"))
    data = data_query.all()

    # processed_data of the form
    # (group_id, file_path) -> (file_path, num_bytes, thumbnails)
    processed_data = {}
    for group_id, file_path, num_bytes, thumb_path, thumb_order in data:
        key = (group_id, file_path)
        if key not in processed_data:
            processed_data[key] = {
                "file_path": file_path,
                "filename": file_path.split("/")[-1],
                "num_bytes": num_bytes,
                "thumbnails": [],
            }
        if thumb_order is not None:
            processed_data[key]["thumbnails"].append((thumb_order, thumb_path))

    # files of the form
    # (group_id, file_path, filename, file_size, thumbnails)
    # or if it's the first file for a group_id, then
    # (group_id, file_path, filename, file_size, thumbnails, rowspan)
    files = []
    unique_group_ids = sorted(set(group_id for group_id, _ in processed_data))
    for group_id in unique_group_ids:
        data_for_group_id = [
            value for key, value in processed_data.items() if key[0] == group_id
        ]
        data_for_group_id.sort(key=lambda x: x["filename"])
        for i, value in enumerate(data_for_group_id):
            # Sorts by thumbnail order
            value["thumbnails"].sort()
            file = {
                "group_id": group_id,
                "file_path": value["file_path"],
                "filename": value["filename"],
                "file_size": convert_size(value["num_bytes"]),
                "thumbnails": [path for _, path in value["thumbnails"]],
            }
            # the first file for every group_id gets the rowspan
            if i == 0:
                file["rowspan"] = len(data_for_group_id)
            files.append(file)

    return render_template(
        "index.html",
        files=files,
        filename_filter=filename_filter,
        extension_filter=extension_filter,
    )


@view_blueprint.route("/group/<group_id>")
def group_page(group_id):
    data = (
        db.session.query(
            File.file_path,
            FileData.num_bytes,
            Thumbnail.path,
            Thumbnail.order,
        )
        .outerjoin(FileData, File.md5 == FileData.md5)
        .outerjoin(Thumbnail, File.md5 == Thumbnail.md5)
        .filter(File.group_id == group_id)
        .all()
    )

    processed_data = {}
    for file_path, num_bytes, thumb_path, thumb_order in data:
        if file_path not in processed_data:
            processed_data[file_path] = {
                "num_bytes": num_bytes,
                "thumbnails": [],
            }
        if thumb_order is not None:
            processed_data[file_path]["thumbnails"].append((thumb_order, thumb_path))

    files = []
    for file_path in sorted(processed_data):
        value = processed_data[file_path]
        value["thumbnails"].sort()
        # assuming Posix path
        posix_path = PurePosixPath(file_path)
        file = {
            "file_path": file_path,
            "directory": str(posix_path.parent),
            "filename": posix_path.name,
            "file_size": convert_size(value["num_bytes"]),
            "thumbnails": [path for _, path in value["thumbnails"]],
        }
        files.append(file)

    return render_template("group.html", group_id=group_id, files=files)


@view_blueprint.route("/group/<group_id>/file/<path:file_path>")
def file_page(group_id, file_path):
    filename = PurePosixPath(file_path).name
    return render_template(
        "file.html", group_id=group_id, file_path=file_path, filename=filename
    )
