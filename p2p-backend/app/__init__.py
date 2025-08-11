from flask import Flask
from flask_cors import CORS
from .routes.api_routes import api_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix="/api")

    return app
