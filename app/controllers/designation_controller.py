from flask import request
from flask_restx import Namespace, Resource

from app.schemas.swagger_models import create_designation_model, create_error_model
from app.services.designation_service import DesignationService
from app.utils.auth import token_required

from .error_handlers import abort_app_error


designation_ns = Namespace(
    "Designations",
    path="/designations",
    description="Designation Management",
)
designation_model = create_designation_model(designation_ns)
error_model = create_error_model(designation_ns)
designation_service = DesignationService()


@designation_ns.route("")
@designation_ns.doc(security="Bearer Auth")
class DesignationListResource(Resource):
    @designation_ns.marshal_list_with(designation_model)
    @token_required
    def get(self):
        """List designations."""
        try:
            return designation_service.list_designations()
        except Exception as exc:
            abort_app_error(designation_ns, exc)

    @designation_ns.expect(designation_model, validate=True)
    @designation_ns.marshal_with(designation_model, code=201)
    @designation_ns.response(409, "Duplicate designation", error_model)
    @token_required
    def post(self):
        """Create a designation."""
        try:
            return designation_service.create_designation(request.get_json() or {}), 201
        except Exception as exc:
            abort_app_error(designation_ns, exc)


@designation_ns.route("/<int:designation_id>")
@designation_ns.param("designation_id", "Designation id")
@designation_ns.doc(security="Bearer Auth")
class DesignationResource(Resource):
    @designation_ns.marshal_with(designation_model)
    @token_required
    def get(self, designation_id):
        """Get a designation."""
        try:
            return designation_service.get_designation(designation_id)
        except Exception as exc:
            abort_app_error(designation_ns, exc)

    @designation_ns.expect(designation_model, validate=False)
    @designation_ns.marshal_with(designation_model)
    @token_required
    def put(self, designation_id):
        """Update a designation."""
        try:
            return designation_service.update_designation(
                designation_id,
                request.get_json() or {},
            )
        except Exception as exc:
            abort_app_error(designation_ns, exc)

    @designation_ns.response(204, "Deleted")
    @token_required
    def delete(self, designation_id):
        """Delete a designation."""
        try:
            designation_service.delete_designation(designation_id)
            return "", 204
        except Exception as exc:
            abort_app_error(designation_ns, exc)
