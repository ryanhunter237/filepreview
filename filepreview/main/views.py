import os

from flask import Blueprint, render_template

from .models import db, File, FileData, Thumbnail


view_blueprint = Blueprint("view", __name__)


from flask import send_from_directory, abort


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
    data = (
        db.session.query(
            File.group_id,
            File.file_path,
            FileData.num_bytes,
            Thumbnail.path,
            Thumbnail.order,
        )
        .join(FileData, File.md5 == FileData.md5)
        .join(Thumbnail, File.md5 == Thumbnail.md5)
        .order_by(Thumbnail.order)
        .all()
    )

    # Process data to group thumbnails by md5
    processed_data = {}
    for group_id, file_path, num_bytes, thumb_path, thumb_order in data:
        filename = file_path.split("/")[-1]  # Assumes UNIX-like file paths
        if group_id not in processed_data:
            processed_data[group_id] = {
                "filename": filename,
                "num_bytes": num_bytes,
                "thumbnails": [],
            }
        processed_data[group_id]["thumbnails"].append((thumb_order, thumb_path))

    # Convert dict to list and sort thumbnails
    final_data = []
    for key, value in processed_data.items():
        value["thumbnails"].sort()  # Sorts by thumbnail order
        final_data.append(
            {
                "group_id": key,
                "filename": value["filename"],
                "num_bytes": value["num_bytes"],
                "thumbnails": [path for order, path in value["thumbnails"]],
            }
        )

    return render_template("index.html", files=final_data)
