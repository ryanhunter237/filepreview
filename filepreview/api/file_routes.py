from typing import Any

from flask import Blueprint, request, jsonify, Response
from sqlalchemy.exc import SQLAlchemyError

from ..models.models import db, File, FileData

file_blueprint = Blueprint("file", __name__)


def add_to_database(data: dict[str, Any], model_cls) -> tuple[Response, int]:
    try:
        model_instance = model_cls(**data)
        db.session.add(model_instance)
        db.session.commit()
        return jsonify({"message": f"{model_cls.__name__} added successfully"}), 201
    except KeyError as e:
        return jsonify({"error": "Data error", "message": str(e)}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Processing error", "message": str(e)}), 500


@file_blueprint.route("/api/file", methods=["POST"])
def add_file() -> tuple[Response, int]:
    data = request.json
    return add_to_database(data, File)


@file_blueprint.route("/api/files/<group_id>", methods=["GET"])
def get_files_by_group_id(group_id: str) -> Response:
    files: list[File] = File.query.filter_by(group_id=group_id).all()
    return jsonify(
        [
            {"group_id": file.group_id, "file_path": file.file_path, "md5": file.md5}
            for file in files
        ]
    )


@file_blueprint.route("/api/file-data", methods=["POST"])
def add_file_data() -> tuple[Response, int]:
    data = request.json
    return add_to_database(data, FileData)
