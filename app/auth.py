import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta

# -----------------------------------
# Generate JWT Token (Login simulation)
# -----------------------------------
def generate_token():
    payload = {
        "user": "admin",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGORITHM"]
    )

    return token


# -----------------------------------
# JWT Decorator
# -----------------------------------
def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "JWT token missing"}), 401

        try:
            jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=[current_app.config["JWT_ALGORITHM"]]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403

        return func(*args, **kwargs)

    return wrapper
