from flask import request
from flask_restx import Namespace, Resource

from app.schemas.swagger_models import create_error_model, create_organisation_model
from app.services.organisation_service import OrganisationService
from app.utils.auth import token_required

from .error_handlers import abort_app_error


organisation_ns = Namespace(
    "Organisations",
    path="/organisations",
    description="Organisation Management",
)
organisation_model = create_organisation_model(organisation_ns)
error_model = create_error_model(organisation_ns)
organisation_service = OrganisationService()


@organisation_ns.route("")
@organisation_ns.doc(security="Bearer Auth")
class OrganisationListResource(Resource):
    @organisation_ns.marshal_list_with(organisation_model)
    @token_required
    def get(self):
        """List organisations."""
        try:
            return organisation_service.list_organisations()
        except Exception as exc:
            return abort_app_error(organisation_ns, exc)

    @organisation_ns.expect(organisation_model, validate=False)
    @organisation_ns.marshal_with(organisation_model, code=201)
    @organisation_ns.response(409, "Duplicate organisation", error_model)
    @token_required
    def post(self):
        """Create an organisation."""
        try:
            return organisation_service.create_organisation(request.get_json() or {}), 201
        except Exception as exc:
            return abort_app_error(organisation_ns, exc)


@organisation_ns.route("/<int:organisation_id>")
@organisation_ns.param("organisation_id", "Organisation id")
@organisation_ns.doc(security="Bearer Auth")
class OrganisationResource(Resource):
    @organisation_ns.marshal_with(organisation_model)
    @token_required
    def get(self, organisation_id):
        """Get an organisation."""
        try:
            return organisation_service.get_organisation(organisation_id)
        except Exception as exc:
            return abort_app_error(organisation_ns, exc)

    @organisation_ns.expect(organisation_model, validate=False)
    @organisation_ns.marshal_with(organisation_model)
    @token_required
    def put(self, organisation_id):
        """Update an organisation."""
        try:
            return organisation_service.update_organisation(
                organisation_id,
                request.get_json() or {},
            )
        except Exception as exc:
            return abort_app_error(organisation_ns, exc)

    @organisation_ns.response(204, "Deleted")
    @token_required
    def delete(self, organisation_id):
        """Delete an organisation."""
        try:
            organisation_service.delete_organisation(organisation_id)
            return "", 204
        except Exception as exc:
            return abort_app_error(organisation_ns, exc)
