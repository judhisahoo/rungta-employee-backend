from flask import Flask
from flask_cors import CORS

from .config import Config
from .controllers.auth_controller import auth_ns
from .controllers.designation_controller import designation_ns
from .controllers.employee_controller import employee_ns
from .controllers.organisation_controller import organisation_ns
from .extensions import api, db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    api.add_namespace(auth_ns)
    api.add_namespace(organisation_ns)
    api.add_namespace(designation_ns)
    api.add_namespace(employee_ns)

    return app
