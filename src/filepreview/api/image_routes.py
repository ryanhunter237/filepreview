from flask import Blueprint, request, jsonify, url_for

from ..main.models import db, Thumbnail, Image, File
from .utils import add_to_database


image_blueprint = Blueprint("image", __name__)


@image_blueprint.route("/api/thumbnail", methods=["POST"])
def add_thumbnail():
    """data must have keys md5, order, and path"""
    data = request.json
    return add_to_database(data, Thumbnail)


@image_blueprint.route("/api/image", methods=["POST"])
def add_image():
    """data must have keys md5, order, and path"""
    data = request.json
    return add_to_database(data, Image)


@image_blueprint.route("/api/images", methods=["GET"])
def get_images():
    group_id = request.args.get("group_id")
    directory = request.args.get("directory")
    filename = request.args.get("filename")
    data = (
        db.session.query(
            Image.order,
            Image.path,
        )
        .join(File, File.md5 == Image.md5)
        .filter(File.group_id == group_id)
        .filter(File.directory == directory)
        .filter(File.filename == filename)
        .all()
    )
    image_urls = [
        url_for("view.serve_image", filepath=path) for _, path in sorted(data)
    ]
    return jsonify(image_urls)
