# app/auth.py
import jwt
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from app.models import User

auth_bp = Blueprint("auth", __name__)

# -------------------------
# JWT Helpers
# -------------------------
def generate_token(user):
    payload = {
        "user_id": user.id,
        "is_admin": user.is_admin,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = payload["user_id"]
            request.is_admin = payload["is_admin"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

# -------------------------
# Flexible RBAC Decorator
# -------------------------
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_role = "admin" if getattr(request, "is_admin", False) else "user"
            if user_role not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator
