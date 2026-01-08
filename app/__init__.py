from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Import models so SQLAlchemy knows them
    from app import models

    # Import and register API blueprint
    from app.routes import api
    app.register_blueprint(api, url_prefix="/api")

    # Health check route
    @app.route("/")
    def home():
        return jsonify({
            "status": "running",
            "message": "Student Performance API is live"
        })

    return app



