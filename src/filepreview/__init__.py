from flask import Flask

from .main.models import db
from .api.file_routes import file_blueprint
from .api.image_routes import image_blueprint
from .main.views import view_blueprint


def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.config.from_object("filepreview.config")
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(file_blueprint)
    app.register_blueprint(image_blueprint)
    app.register_blueprint(view_blueprint)

    with app.app_context():
        db.create_all()

    return app
