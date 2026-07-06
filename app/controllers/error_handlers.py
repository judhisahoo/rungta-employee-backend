import json

from flask import current_app, jsonify
from werkzeug.exceptions import HTTPException

from app.utils.exceptions import AppError


def abort_app_error(namespace, exc):
    if isinstance(exc, AppError):
        raise exc
    raise exc


def handle_app_error(exc):
    return error_response(exc.message, exc.status_code)


def handle_restx_app_error(exc):
    return {"message": exc.message, "status_code": exc.status_code}, exc.status_code


def error_response(message, status_code):
    response = jsonify({"message": message, "status_code": status_code})
    response.status_code = status_code
    return response


def handle_http_exception(exc):
    status_code = exc.code or 500
    message = "Resource not found" if status_code == 404 else exc.description
    return error_response(message, status_code)


def handle_unexpected_exception(exc):
    current_app.logger.exception("Unhandled exception", exc_info=exc)
    return error_response("Internal server error", 500)


def add_status_code_to_json_response(response):
    if not response.is_json:
        return response

    data = response.get_json(silent=True)
    if isinstance(data, dict) and "status_code" not in data:
        data["status_code"] = response.status_code
        response.set_data(json.dumps(data))

    return response
