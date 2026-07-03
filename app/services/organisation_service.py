from app.models import Organisation
from app.repositories.organisation_repository import OrganisationRepository
from app.utils.exceptions import NotFoundError, ValidationError


class OrganisationService:
    def __init__(self, organisation_repository=None):
        self.organisation_repository = (
            organisation_repository or OrganisationRepository()
        )

    def list_organisations(self):
        return [
            organisation.to_dict()
            for organisation in self.organisation_repository.list_all()
        ]

    def get_organisation(self, organisation_id):
        return self._get_or_raise(organisation_id).to_dict()

    def create_organisation(self, payload):
        organisation = Organisation()
        self._apply_payload(organisation, payload or {})
        self.organisation_repository.add(organisation)
        self.organisation_repository.commit()
        return organisation.to_dict()

    def update_organisation(self, organisation_id, payload):
        organisation = self._get_or_raise(organisation_id)
        self._apply_payload(organisation, payload or {})
        self.organisation_repository.commit()
        return organisation.to_dict()

    def delete_organisation(self, organisation_id):
        organisation = self._get_or_raise(organisation_id)
        self.organisation_repository.delete(organisation)
        self.organisation_repository.commit()

    def _get_or_raise(self, organisation_id):
        organisation = self.organisation_repository.get_by_id(organisation_id)
        if not organisation:
            raise NotFoundError("Organisation not found")
        return organisation

    def _apply_payload(self, organisation, payload):
        if "name" in payload:
            organisation.name = payload["name"]

        if "parent_id" not in payload:
            return

        parent_id = payload.get("parent_id")
        if parent_id in (0, "", None):
            organisation.parent_id = None
            return

        if parent_id == organisation.id:
            raise ValidationError("Organisation cannot be its own parent")

        if not self.organisation_repository.get_by_id(parent_id):
            raise NotFoundError("Parent organisation not found")

        organisation.parent_id = parent_id

