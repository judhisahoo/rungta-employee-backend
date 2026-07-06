from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .config import Config
from .controllers.auth_controller import auth_ns
from .controllers.designation_controller import designation_ns
from .controllers.employee_controller import employee_ns
from .controllers.error_handlers import (
    add_status_code_to_json_response,
    handle_app_error,
    handle_http_exception,
    handle_restx_app_error,
    handle_unexpected_exception,
)
from .controllers.organisation_controller import organisation_ns
from .extensions import api, db, migrate
from .utils.exceptions import AppError


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    app.register_error_handler(AppError, handle_app_error)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_unexpected_exception)
    api.errorhandler(AppError)(handle_restx_app_error)
    app.after_request(add_status_code_to_json_response)

    api.add_namespace(auth_ns)
    api.add_namespace(organisation_ns)
    api.add_namespace(designation_ns)
    api.add_namespace(employee_ns)

    return app
