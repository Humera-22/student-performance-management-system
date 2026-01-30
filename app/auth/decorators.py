"""
import jwt
from functools import wraps
from flask import request, jsonify, g, current_app
from app.auth.permissions import ROLE_PERMISSION_MAP
from app.exceptions import UnauthorizedException, ForbiddenException
from app.models import User

# ------------------------
# JWT TOKEN DECORATOR
# ------------------------
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if not token:
            raise UnauthorizedException("Token missing")

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user = User.query.get(payload["user_id"])
            if not user:
                raise UnauthorizedException("User not found")
            g.user = user
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Invalid token")

        return f(*args, **kwargs)
    return wrapper

# ------------------------
# PERMISSION DECORATOR
# ------------------------
def permission_required(permission):
    
    Checks if the logged-in user's role has the required permission.
    Usage:
        @jwt_required
        @permission_required(PERMISSIONS["STUDENT_CREATE"])
    
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = getattr(g, "user", None)
            if not user:
                raise UnauthorizedException("User not found in context")
            
            role = user.role
            allowed_permissions = ROLE_PERMISSION_MAP.get(role, [])
            if permission not in allowed_permissions:
                raise ForbiddenException(f"Access denied for role '{role}'")

            return f(*args, **kwargs)
        return wrapped
    return decorator
"""
"""
# app/auth/decorators.py
from functools import wraps
from flask import request, g
import jwt
from app.auth.permissions import ROLE_PERMISSION_MAP
from app.exceptions import UnauthorizedException, ForbiddenException
from flask import current_app

# ------------------------
# JWT TOKEN DECORATOR
# ------------------------
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if not token:
            raise UnauthorizedException("Token missing")

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            # Save payload in request context
            g.user_id = payload["user_id"]
            g.roles = payload.get("roles", [])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Invalid token")

        return f(*args, **kwargs)
    return wrapper

# ------------------------
# PERMISSION DECORATOR
# ------------------------
def permission_required(permission):
    
    Checks if any of the user's roles has the required permission.
    Usage:
        @jwt_required
        @permission_required(PERMISSIONS["STUDENT_CREATE"])
    
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            roles = getattr(g, "roles", [])
            if not roles:
                raise UnauthorizedException("User roles not found in token")

            # Check if any role has the required permission
            allowed = False
            for role in roles:
                permissions = ROLE_PERMISSION_MAP.get(role, [])
                if permission in permissions:
                    allowed = True
                    break

            if not allowed:
                raise ForbiddenException(f"Access denied for roles: {roles}")

            return f(*args, **kwargs)
        return wrapped
    return decorator
"""
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
