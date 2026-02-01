# app/auth/decorators.py
from functools import wraps
from flask import request, g
import jwt
from flask import current_app
from app.exceptions import UnauthorizedException, ForbiddenException

def jwt_required(f):
    """Check if JWT is valid and extract user info"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if not token:
            raise UnauthorizedException("Token missing")

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            g.user_id = payload["user_id"]
            g.roles = payload.get("roles", [])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Invalid token")

        return f(*args, **kwargs)
    return wrapper


def roles_required(allowed_roles):
    """
    Check if the user has at least one of the allowed roles.
    Example usage:
        @jwt_required
        @roles_required(["admin", "teacher"])
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            roles = getattr(g, "roles", [])
            if not roles:
                raise UnauthorizedException("User roles missing in token")

            if not any(role in allowed_roles for role in roles):
                raise ForbiddenException(f"Access denied. Required roles: {allowed_roles}")

            return f(*args, **kwargs)
        return wrapped
    return decorator
