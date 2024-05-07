from flask import Blueprint, request

from ..main.models import Thumbnail, Image
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
