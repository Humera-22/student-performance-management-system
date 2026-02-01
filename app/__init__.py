from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.exceptions import AppException 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # Global exception handling
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
        "error": str(error),
        "type": error.__class__.__name__
    }), 500


    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    @app.route("/")
    def health():
        return jsonify({"status": "running"})

    return app
