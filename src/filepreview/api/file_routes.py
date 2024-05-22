from flask import Blueprint, request, jsonify, abort

from ..main.models import File, FileData, Program, db
from .utils import add_to_database

file_blueprint = Blueprint("file", __name__)


@file_blueprint.route("/api/file", methods=["POST"])
def add_file():
    """data must have keys group_id, file_path, and md5"""
    data = request.json
    return add_to_database(data, File)


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
