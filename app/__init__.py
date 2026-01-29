from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app import models

    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def home():
        return jsonify({
            "status": "running",
            "message": "Student Performance API is live"
        })

    return app


