"""
import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    # ✅ FIX: ensure string
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token
"""
"""
# app/auth/jwt.py
import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user):
    
    Generates JWT token containing user_id and roles (list of roles).
    Token expires in 1 hour.
    
    payload = {
        "user_id": user.id,
        "roles": getattr(user, "roles", [getattr(user, "role", "user")]),  # support multiple roles
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    # Ensure string
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token
"""
# app/auth/jwt.py
import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user):
    """
    Generate JWT token with multiple roles.
    Payload example:
    {
        "user_id": 1,
        "roles": ["admin", "teacher"],
        "exp": <expiry timestamp>
    }
    """
    payload = {
        "user_id": user.id,
        "roles": user.roles,  # list of roles
        "exp": datetime.utcnow() + timedelta(hours=1),
        "token_type": "access"
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    # Ensure token is string for JSON response
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token
