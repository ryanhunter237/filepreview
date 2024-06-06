from flask import Blueprint, request, jsonify, abort, url_for

from ..main.models import File, FileData, Program, db, Thumbnail
from .utils import add_to_database

file_blueprint = Blueprint("file", __name__)


@file_blueprint.route("/api/file", methods=["POST"])
def add_file():
    """data must have keys group_id, directory, filename, and md5"""
    data = request.json
    return add_to_database(data, File)


def convert_size(size: int):
    size = float(size)
    suffixes = ["B", "KB", "MB", "GB"]
    suffix_idx = 0
    while size >= 1024 and suffix_idx < 3:
        size /= 1024
        suffix_idx += 1
    return f"{round(size)} {suffixes[suffix_idx]}"


@file_blueprint.route("/api/files", methods=["GET"])
def get_files():
    filename_filter = request.args.get("filename", "").strip()
    extension_filter = request.args.get("extension", "").strip()

    data_query = (
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
    if filename_filter:
        data_query = data_query.filter(File.filename.ilike(f"%{filename_filter}%"))
    if extension_filter:
        data_query = data_query.filter(File.filename.ilike(f"%{extension_filter}"))

    data = data_query.all()
    processed_data = {}
    for group_id, directory, filename, num_bytes, thumb_path, thumb_order in data:
        if group_id not in processed_data:
            processed_data[group_id] = {
                "group_url": url_for("view.group_page", group_id=group_id),
                "files": {},
            }
        files = processed_data[group_id]["files"]
        key = (directory, filename)
        if key not in files:
            files[key] = {
                "filename": filename,
                "file_url": url_for(
                    "view.file_page",
                    group_id=group_id,
                    directory=directory,
                    filename=filename,
                ),
                "file_size": convert_size(num_bytes),
                "thumbnails": [],
            }
        if thumb_path:
            files[key]["thumbnails"].append(
                {
                    "thumbnail_order": thumb_order,
                    "thumbnail_url": url_for("view.serve_image", filepath=thumb_path),
                }
            )

    formatted_data = {}
    for group_id, group_data in processed_data.items():
        formatted_data[group_id] = {
            "group_url": group_data["group_url"],
            "files": get_formatted_files_in_order(group_data["files"]),
        }

    return formatted_data


def get_formatted_files_in_order(files: dict[tuple, dict]) -> list[dict[str, str]]:
    sorted_file_keys = sorted(files)  # sorted by (directory, filename)
    formatted_files = []
    for key in sorted_file_keys:
        file = files[key]
        formatted_files.append(
            {
                "filename": file["filename"],
                "file_url": file["file_url"],
                "file_size": file["file_size"],
                "thumbnail_urls": get_thumbnail_urls_in_order(file["thumbnails"]),
            }
        )
    return formatted_files


def get_thumbnail_urls_in_order(thumbnails: list[dict]) -> list[str]:
    sorted_thumbnails = sorted(thumbnails, key=lambda d: d["thumbnail_order"])
    return [d["thumbnail_url"] for d in sorted_thumbnails]


@file_blueprint.route("/api/file-data", methods=["POST"])
def add_file_data():
    """data must have keys md5, num_bytes, and local_path
    Can optionally include program
    """
    data = request.json
    return add_to_database(data, FileData)


@file_blueprint.route("/api/file-data", methods=["PUT"])
def update_file_data():
    """data must have keys md5 and program"""
    data = request.json
    record = FileData.query.get(data["md5"])
    if record:
        record.program = data["program"]
        db.session.commit()
        return jsonify({"message": "FileData updated successfully"}), 200
    else:
        return jsonify({"message": "FileData not found for md5"}), 404


@file_blueprint.route("/api/program", methods=["POST"])
def add_program():
    """data must have keys name and executable"""
    data = request.json
    return add_to_database(data, Program)


@file_blueprint.route("/api/program/<md5>", methods=["GET"])
def get_program(md5: str):
    data = (
        db.session.query(
            FileData.local_path,
            Program.name,
            Program.executable,
        )
        .join(FileData, Program.name == FileData.program)
        .filter(FileData.md5 == md5)
        .first()
    )

    if data is None:
        abort(404, description="No program found for the file with given md5 hash")

    return jsonify(
        {
            "local_path": data.local_path,
            "program_name": data.name,
            "program_exe": data.executable,
        }
    )
