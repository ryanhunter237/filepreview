from flask import Blueprint, request, jsonify, Response

from ..main.models import File, FileData
from .utils import add_to_database

file_blueprint = Blueprint("file", __name__)


@file_blueprint.route("/api/file", methods=["POST"])
def add_file():
    """data must have keys group_id, file_path, and md5"""
    data = request.json
    return add_to_database(data, File)


@file_blueprint.route("/api/files/<group_id>", methods=["GET"])
def get_files_by_group_id(group_id: str):
    files: list[File] = File.query.filter_by(group_id=group_id).all()
    return jsonify(
        [
            {"group_id": file.group_id, "file_path": file.file_path, "md5": file.md5}
            for file in files
        ]
    )


@file_blueprint.route("/api/file-data", methods=["POST"])
def add_file_data():
    """data must have keys md5, num_bytes, and local_path"""
    data = request.json
    return add_to_database(data, FileData)
