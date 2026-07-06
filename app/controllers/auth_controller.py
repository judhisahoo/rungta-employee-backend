from flask import request
from flask_restx import Namespace, Resource

from app.schemas.swagger_models import (
    create_employee_model,
    create_login_error_model,
    create_login_model,
    create_login_success_model,
    create_register_model,
)
from app.services.auth_service import AuthService

from .error_handlers import abort_app_error


auth_ns = Namespace("Auth", path="/auth", description="Authentication")
login_model = create_login_model(auth_ns)
auth_employee_model = create_employee_model(auth_ns)
register_model = create_register_model(auth_ns)
login_success_model = create_login_success_model(auth_ns, auth_employee_model)
login_error_model = create_login_error_model(auth_ns)
auth_service = AuthService()


@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.response(200, "Login successful", login_success_model)
    @auth_ns.response(402, "Invalid credential", login_error_model)
    def post(self):
        """Login using email and password."""
        response = auth_service.login(request.get_json() or {})
        if response.get("status_code") == 402:
            return response, 402
        return response, 200


@auth_ns.route("/register")
class RegisterResource(Resource):
    @auth_ns.expect(register_model, validate=True)
    @auth_ns.marshal_with(auth_employee_model, code=201)
    def post(self):
        """Register an employee."""
        try:
            return auth_service.register(request.get_json() or {}), 201
        except Exception as exc:
            return abort_app_error(auth_ns, exc)
