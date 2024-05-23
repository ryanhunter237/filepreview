import os
import subprocess

from flask import (
    Blueprint,
    render_template,
    request,
    send_from_directory,
    abort,
)

from .models import db, File, FileData, Thumbnail

view_blueprint = Blueprint("view", __name__)


def convert_size(size: int):
    size = float(size)
    suffixes = ["B", "KB", "MB", "GB"]
    suffix_idx = 0
    while size >= 1024 and suffix_idx < 3:
        size /= 1024
        suffix_idx += 1
    return f"{round(size)} {suffixes[suffix_idx]}"


def get_data_query():
    return (
        db.session.query(
            File.group_id,
            File.directory,
            File.filename,
            FileData.num_bytes,
            Thumbnail.path,
            Thumbnail.order,
        )
        .outerjoin(FileData, File.md5 == FileData.md5)
        .outerjoin(Thumbnail, File.md5 == Thumbnail.md5)
    )


def process_data(data, include_group_id=True):
    processed_data = {}
    for record in data:
        if include_group_id:
            group_id, directory, filename, num_bytes, thumb_path, thumb_order = record
            key = (group_id, directory, filename)
        else:
            directory, filename, num_bytes, thumb_path, thumb_order = record[1:]
            key = (directory, filename)

        if key not in processed_data:
            processed_data[key] = {
                "directory": directory,
                "filename": filename,
                "num_bytes": num_bytes,
                "thumbnails": [],
            }
        if thumb_order is not None:
            processed_data[key]["thumbnails"].append((thumb_order, thumb_path))
    return processed_data


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
    extension_filter = request.args.get("extension", "").strip()

    data_query = get_data_query()
    if filename_filter:
        data_query = data_query.filter(File.filename.ilike(f"%{filename_filter}%"))
    if extension_filter:
        data_query = data_query.filter(File.filename.ilike(f"%{extension_filter}"))

    data = data_query.all()
    processed_data = process_data(data, include_group_id=True)
    files = organize_files_for_index(processed_data)

    return render_template(
        "index.html",
        files=files,
        filename_filter=filename_filter,
        extension_filter=extension_filter,
    )


def organize_files_for_index(processed_data):
    files = []
    unique_group_ids = sorted(set(group_id for group_id, *_ in processed_data))
    for group_id in unique_group_ids:
        data_for_group_id = [
            value for key, value in processed_data.items() if key[0] == group_id
        ]
        data_for_group_id.sort(key=lambda x: x["filename"])
        for i, value in enumerate(data_for_group_id):
            value["thumbnails"].sort()
            file = {
                "group_id": group_id,
                "directory": value["directory"],
                "filename": value["filename"],
                "file_size": convert_size(value["num_bytes"]),
                "thumbnails": [path for _, path in value["thumbnails"]],
            }
            if i == 0:
                file["rowspan"] = len(data_for_group_id)
            files.append(file)
    return files


@view_blueprint.route("/group", methods=["GET"])
def group_page():
    group_id = request.args.get("group_id", "").strip()
    data = get_data_query().filter(File.group_id == group_id).all()
    processed_data = process_data(data, include_group_id=False)
    files = organize_files_for_group(processed_data)

    return render_template("group.html", group_id=group_id, files=files)


def organize_files_for_group(processed_data):
    files = []
    for key in sorted(processed_data):
        value = processed_data[key]
        value["thumbnails"].sort()
        directory, filename = key
        file = {
            "directory": directory,
            "filename": filename,
            "file_size": convert_size(value["num_bytes"]),
            "thumbnails": [path for _, path in value["thumbnails"]],
        }
        files.append(file)
    return files


@view_blueprint.route("/file")
def file_page():
    group_id = request.args.get("group_id").strip()
    directory = request.args.get("directory").strip()
    filename = request.args.get("filename").strip()

    result = (
        db.session.query(File.md5)
        .filter(File.group_id == group_id)
        .filter(File.directory == directory)
        .filter(File.filename == filename)
        .first()
    )

    if result is None:
        abort(404, description="No md5 hash found for this file")

    return render_template(
        "file.html",
        group_id=group_id,
        directory=directory,
        filename=filename,
        md5=result.md5,
    )


@view_blueprint.route("/launch")
def launch():
    application = request.args.get("application", "").strip()
    local_path = request.args.get("local_path", "").strip()
    if os.path.exists(local_path):
        subprocess.call([application, local_path])
        return "File opened", 200
    return "File not found", 404
