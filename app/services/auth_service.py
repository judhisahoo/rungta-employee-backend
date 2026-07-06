import base64
from datetime import datetime, timedelta

import jwt
from flask import current_app

from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.utils.validators import is_blank, normalize_blank


class AuthService:
    def __init__(self, employee_repository=None, employee_service=None):
        self.employee_repository = employee_repository or EmployeeRepository()
        self.employee_service = employee_service or EmployeeService()

    def login(self, payload):
        email = normalize_blank((payload or {}).get("email"))
        password = normalize_blank((payload or {}).get("password"))

        if is_blank(email) or is_blank(password):
            return self._invalid_credentials_response()

        employee = self.employee_repository.get_by_email(email)
        if not employee or not self._password_matches(employee.password, password):
            return self._invalid_credentials_response()

        user = employee.to_dict()
        return {
            "status": 200,
            "status_code": 200,
            "user": user,
            "access_token": self._build_token(employee, "access"),
            "refresh_token": self._build_token(employee, "refresh"),
        }

    def register(self, payload):
        return self.employee_service.create_employee(payload or {})

    def _password_matches(self, stored_password, provided_password):
        if not stored_password or not provided_password:
            return False
        provided_password = str(provided_password).strip()
        if stored_password == provided_password:
            return True
        encoded_password = base64.b64encode(
            provided_password.encode("utf-8")
        ).decode("utf-8")
        return stored_password == encoded_password

    def _build_token(self, employee, token_type):
        now = datetime.utcnow()
        if token_type == "refresh":
            expires_at = now + timedelta(
                days=current_app.config["JWT_REFRESH_TOKEN_EXPIRES_DAYS"]
            )
        else:
            expires_at = now + timedelta(
                minutes=current_app.config["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"]
            )

        payload = {
            "sub": str(employee.id),
            "email": employee.email,
            "employee_code": employee.employee_code,
            "type": token_type,
            "iat": now,
            "exp": expires_at,
        }
        return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    def _invalid_credentials_response(self):
        return {
            "message": "Invalid credential",
            "status_code": 402,
        }
