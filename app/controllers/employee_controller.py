from flask import request
from flask_restx import Namespace, Resource

from app.schemas.swagger_models import (
    create_employee_model,
    create_employee_search_model,
    create_error_model,
    create_generate_id_response_model,
    create_validate_id_card_no_model,
    create_validate_id_card_no_response_model,
)
from app.services.employee_service import EmployeeService
from app.utils.auth import token_required

from .error_handlers import abort_app_error


employee_ns = Namespace("Employees", path="/employees", description="Employee Management")
employee_model = create_employee_model(employee_ns)
employee_search_model = create_employee_search_model(employee_ns)
generate_id_response_model = create_generate_id_response_model(employee_ns)
validate_id_card_no_model = create_validate_id_card_no_model(employee_ns)
validate_id_card_no_response_model = create_validate_id_card_no_response_model(
    employee_ns
)
error_model = create_error_model(employee_ns)
employee_service = EmployeeService()


@employee_ns.route("")
@employee_ns.doc(security="Bearer Auth")
class EmployeeListResource(Resource):
    @employee_ns.marshal_list_with(employee_model)
    @token_required
    def get(self):
        """List employees."""
        try:
            organisation_id = request.args.get("organisation_id", type=int)
            return employee_service.list_employees(organisation_id)
        except Exception as exc:
            abort_app_error(employee_ns, exc)

    @employee_ns.expect(employee_model, validate=True)
    @employee_ns.marshal_with(employee_model, code=201)
    @employee_ns.response(409, "Duplicate employee", error_model)
    @token_required
    def post(self):
        """Create an employee."""
        try:
            return employee_service.create_employee(request.get_json() or {}), 201
        except Exception as exc:
            abort_app_error(employee_ns, exc)


@employee_ns.route("/generate_id")
@employee_ns.doc(security="Bearer Auth")
class EmployeeGenerateIdResource(Resource):
    @employee_ns.marshal_with(generate_id_response_model)
    @token_required
    def post(self):
        """Generate a unique employee ID card number."""
        try:
            return employee_service.generate_unique_id_card_no()
        except Exception as exc:
            abort_app_error(employee_ns, exc)


@employee_ns.route("/validate_id_card_no")
@employee_ns.doc(security="Bearer Auth")
class EmployeeValidateIdCardNoResource(Resource):
    @employee_ns.expect(validate_id_card_no_model, validate=True)
    @employee_ns.marshal_with(validate_id_card_no_response_model)
    @token_required
    def post(self):
        """Validate whether an employee ID card number already exists."""
        try:
            return employee_service.validate_id_card_no(request.get_json() or {})
        except Exception as exc:
            abort_app_error(employee_ns, exc)


@employee_ns.route("/search")
@employee_ns.doc(security="Bearer Auth")
class EmployeeSearchResource(Resource):
    @employee_ns.expect(employee_search_model, validate=True)
    @employee_ns.marshal_with(employee_model)
    @token_required
    def post(self):
        """Search employee by ID card number."""
        try:
            return employee_service.search_employee_by_id_card_no(
                request.get_json() or {}
            )
        except Exception as exc:
            abort_app_error(employee_ns, exc)


@employee_ns.route("/search_by_id_card")
class EmployeeSearchByIdCardResource(Resource):
    @employee_ns.expect(employee_search_model, validate=True)
    @employee_ns.marshal_with(employee_model)
    def post(self):
        """Search employee by ID card number without authentication."""
        try:
            return employee_service.search_employee_by_id_card_no(
                request.get_json() or {}
            )
        except Exception as exc:
            abort_app_error(employee_ns, exc)


@employee_ns.route("/<int:employee_id>")
@employee_ns.param("employee_id", "Employee id")
@employee_ns.doc(security="Bearer Auth")
class EmployeeResource(Resource):
    @employee_ns.marshal_with(employee_model)
    @token_required
    def get(self, employee_id):
        """Get an employee."""
        try:
            return employee_service.get_employee(employee_id)
        except Exception as exc:
            abort_app_error(employee_ns, exc)

    @employee_ns.expect(employee_model, validate=False)
    @employee_ns.marshal_with(employee_model)
    @token_required
    def put(self, employee_id):
        """Update an employee."""
        try:
            return employee_service.update_employee(
                employee_id,
                request.get_json() or {},
            )
        except Exception as exc:
            abort_app_error(employee_ns, exc)

    @employee_ns.response(204, "Deleted")
    @token_required
    def delete(self, employee_id):
        """Delete an employee."""
        try:
            employee_service.delete_employee(employee_id)
            return "", 204
        except Exception as exc:
            abort_app_error(employee_ns, exc)
