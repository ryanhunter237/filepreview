from flask import Flask
from .models.models import db
from .api.file_routes import file_blueprint

def create_app(test_config: dict=None):
    app = Flask(__name__)
    app.config.from_object('filepreview.config')
    if test_config:
        app.config.update(test_config)
    
    db.init_app(app)
    
    app.register_blueprint(file_blueprint)

    return app
