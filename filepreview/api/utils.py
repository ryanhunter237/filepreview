from typing import Any

from flask import Response, jsonify
from sqlalchemy.exc import SQLAlchemyError

from ..main.models import db


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
