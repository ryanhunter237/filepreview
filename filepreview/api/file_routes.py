from flask import Blueprint, request, jsonify
from ..models.models import db, File

file_blueprint = Blueprint("file", __name__)


@file_blueprint.route("/api/file", methods=["POST"])
def add_file():
    data = request.json
    new_file = File(groupid=data["groupid"], filepath=data["filepath"], md5=data["md5"])
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"message": "File added successfully"}), 201


@file_blueprint.route("/api/files/<groupid>", methods=["GET"])
def get_files_by_groupid(groupid):
    files = File.query.filter_by(groupid=groupid).all()
    return jsonify(
        [
            {"groupid": file.groupid, "filepath": file.filepath, "md5": file.md5}
            for file in files
        ]
    )
