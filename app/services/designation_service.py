from app.models import Designation
from app.repositories.designation_repository import DesignationRepository
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.validators import is_blank, normalize_blank


class DesignationService:
    def __init__(self, designation_repository=None):
        self.designation_repository = designation_repository or DesignationRepository()

    def list_designations(self):
        return [
            designation.to_dict()
            for designation in self.designation_repository.list_all()
        ]

    def get_designation(self, designation_id):
        return self._get_or_raise(designation_id).to_dict()

    def create_designation(self, payload):
        designation = Designation()
        self._apply_payload(designation, payload or {})
        self.designation_repository.add(designation)
        self.designation_repository.commit()
        return designation.to_dict()

    def update_designation(self, designation_id, payload):
        designation = self._get_or_raise(designation_id)
        self._apply_payload(designation, payload or {})
        self.designation_repository.commit()
        return designation.to_dict()

    def delete_designation(self, designation_id):
        designation = self._get_or_raise(designation_id)
        self.designation_repository.delete(designation)
        self.designation_repository.commit()

    def _get_or_raise(self, designation_id):
        designation = self.designation_repository.get_by_id(designation_id)
        if not designation:
            raise NotFoundError("Designation not found")
        return designation

    def _apply_payload(self, designation, payload):
        name = normalize_blank(payload.get("name", designation.name))
        if is_blank(name):
            raise ValidationError("Designation name is required")

        designation.name = name
