from functools import wraps

import jwt
from flask import current_app, g, request
from flask_restx import abort


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            abort(401, "Authentication token is missing")

        auth_parts = auth_header.split(None, 1)
        if len(auth_parts) == 2 and auth_parts[0].lower() == "bearer":
            token = auth_parts[1].strip()
        else:
            token = auth_header.strip()

        if not token:
            abort(401, "Authentication token is missing")

        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            abort(401, "Authentication token has expired")
        except jwt.InvalidTokenError:
            abort(401, "Invalid authentication token")

        if payload.get("type") != "access":
            abort(401, "Access token is required")

        g.current_user = payload
        return func(*args, **kwargs)

    return wrapper
