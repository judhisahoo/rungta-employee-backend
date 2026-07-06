import base64
import secrets
import string

from app.models import Employee
from app.repositories.designation_repository import DesignationRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.organisation_repository import OrganisationRepository
from app.utils.exceptions import ConflictError, NotFoundError, ValidationError
from app.utils.validators import is_blank, normalize_blank, parse_date, validate_choice

from .constants import (
    VALID_APP_TYPES,
    VALID_CATEGORIES,
    VALID_EMPLOYMENT_TYPES,
    VALID_GENDERS,
)


class EmployeeService:
    ID_CARD_NO_LENGTH = 16
    ID_CARD_NO_ALPHABET = string.ascii_uppercase + string.digits
    STRICT_REQUIRED_FIELDS = [
        "gender",
        "guardian_name",
        "date_of_birth",
        "place_of_birth",
        "nationality",
        "education_level",
        "date_of_joining",
        "designation",
        "category",
        "mobile_number",
        "employment_type",
        "family_details",
        "posting_details",
        "aadhaar_number",
        "bank_account_no",
        "bank_ifsc",
        "branch",
        "present_address",
        "permanent_address",
        "service_book_no",
    ]
    STRICT_UNIQUE_FIELDS = [
        "universal_account_number",
        "pan",
        "eps_nps",
        "esic_insurance_no",
        "aadhaar_number",
        "bank_account_no",
    ]

    def __init__(
        self,
        employee_repository=None,
        organisation_repository=None,
        designation_repository=None,
    ):
        self.employee_repository = employee_repository or EmployeeRepository()
        self.organisation_repository = (
            organisation_repository or OrganisationRepository()
        )
        self.designation_repository = designation_repository or DesignationRepository()

    def list_employees(self, organisation_id=None):
        if organisation_id:
            employees = self.employee_repository.list_by_organisation_id(
                organisation_id
            )
        else:
            employees = self.employee_repository.list_all()
        return [employee.to_dict() for employee in employees]

    def get_employee(self, employee_id):
        return self._get_or_raise(employee_id).to_dict()

    def search_employee_by_id_card_no(self, payload):
        id_card_no = normalize_blank((payload or {}).get("id_card_no"))
        if is_blank(id_card_no):
            raise ValidationError("id_card_no is required")

        employee = self.employee_repository.get_by_id_card_no(id_card_no)
        if not employee:
            raise NotFoundError("Employee not found")
        return employee.to_dict()

    def generate_unique_id_card_no(self):
        for _ in range(100):
            id_card_no = "".join(
                secrets.choice(self.ID_CARD_NO_ALPHABET)
                for _ in range(self.ID_CARD_NO_LENGTH)
            )
            if not self.employee_repository.get_by_id_card_no(id_card_no):
                return {"id_card_no": id_card_no}

        raise ValidationError("Unable to generate unique id card number")

    def validate_id_card_no(self, payload):
        id_card_no = normalize_blank((payload or {}).get("id_card_number"))
        if is_blank(id_card_no):
            raise ValidationError("id_card_number is required")

        if self.employee_repository.get_by_id_card_no(id_card_no):
            return {
                "exists": True,
                "message": "id card no exists, try another",
            }

        return {
            "exists": False,
            "message": "id card no available",
        }

    def create_employee(self, payload, strict_validation=False):
        employee = Employee()
        self._apply_payload(employee, payload or {})
        if strict_validation:
            self._validate_employee_details(employee)
        self.employee_repository.add(employee)
        self.employee_repository.commit()
        return employee.to_dict()

    def update_employee(self, employee_id, payload, strict_validation=False):
        employee = self._get_or_raise(employee_id)
        self._apply_payload(employee, payload or {})
        if strict_validation:
            self._validate_employee_details(employee)
        self.employee_repository.commit()
        return employee.to_dict()

    def delete_employee(self, employee_id):
        employee = self._get_or_raise(employee_id)
        self.employee_repository.delete(employee)
        self.employee_repository.commit()

    def _get_or_raise(self, employee_id):
        employee = self.employee_repository.get_by_id(employee_id)
        if not employee:
            raise NotFoundError("Employee not found")
        return employee

    def _apply_payload(self, employee, payload):
        for field_name in [
            "employee_code",
            "id_card_no",
            "name",
            "middle_name",
            "surname",
            "gender",
            "guardian_name",
            "place_of_birth",
            "nationality",
            "education_level",
            "mobile_number",
            "email",
            "universal_account_number",
            "pan",
            "nominee",
            "eps_nps",
            "family_details",
            "posting_details",
            "pay",
            "promotion",
            "esic_insurance_no",
            "aadhaar_number",
            "bank_account_no",
            "bank_ifsc",
            "branch",
            "present_address",
            "permanent_address",
            "service_book_no",
            "reason_for_exit",
            "mark_of_identification",
            "photo",
            "specimen_signature_thumb_impression",
            "remarks",
        ]:
            if field_name in payload:
                setattr(employee, field_name, payload[field_name])

        if "date_of_birth" in payload:
            employee.date_of_birth = parse_date(
                payload.get("date_of_birth"), "date_of_birth"
            )
        if "date_of_joining" in payload:
            employee.date_of_joining = parse_date(
                payload.get("date_of_joining"), "date_of_joining"
            )
        if "date_of_exit" in payload:
            employee.date_of_exit = parse_date(
                payload.get("date_of_exit"), "date_of_exit"
            )
        if "gender" in payload:
            employee.gender = validate_choice(
                payload.get("gender"), VALID_GENDERS, "gender"
            )
        if "designation" in payload:
            designation_id = payload.get("designation")
            if designation_id and not self.designation_repository.get_by_id(
                designation_id
            ):
                raise NotFoundError("Designation not found")
            employee.designation = designation_id
        if "category" in payload:
            employee.category = validate_choice(
                payload.get("category"), VALID_CATEGORIES, "category"
            )
        if "employment_type" in payload:
            employee.employment_type = validate_choice(
                payload.get("employment_type"),
                VALID_EMPLOYMENT_TYPES,
                "employment_type",
            )
        if "employee_app_type" in payload:
            employee.employee_app_type = self._normalize_employee_app_type(
                payload.get("employee_app_type")
            )
        if "organisation_id" in payload:
            organisation_id = payload.get("organisation_id")
            if not self.organisation_repository.get_by_id(organisation_id):
                raise NotFoundError("Organisation not found")
            employee.organisation_id = organisation_id
        if "mobile_number" in payload:
            employee.mobile_number = str(payload.get("mobile_number")).strip()
            employee.password = self._build_employee_password(employee.mobile_number)

        if is_blank(employee.mobile_number):
            raise ValidationError("Mobile number is required")

    def _validate_employee_details(self, employee):
        for field_name in self.STRICT_REQUIRED_FIELDS:
            if self._is_empty_value(getattr(employee, field_name)):
                raise ValidationError(
                    "{} is required".format(self._field_label(field_name))
                )

        if employee.date_of_exit and self._is_empty_value(employee.reason_for_exit):
            raise ValidationError(
                "reason for exit is required when date of exit is provided"
            )

        for field_name in self.STRICT_UNIQUE_FIELDS:
            value = normalize_blank(getattr(employee, field_name))
            if self._is_empty_value(value):
                continue

            if self.employee_repository.get_duplicate_value(
                field_name,
                value,
                exclude_employee_id=employee.id,
            ):
                raise ConflictError(
                    "The {} is already exists, Check the data and try again".format(
                        self._field_label(field_name)
                    )
                )

    def _is_empty_value(self, value):
        if isinstance(value, (list, dict, tuple, set)):
            return len(value) == 0
        return is_blank(value)

    def _field_label(self, field_name):
        return field_name.replace("_", " ")

    def _normalize_employee_app_type(self, value):
        value = normalize_blank(value)
        if is_blank(value):
            return "employee"
        if value not in VALID_APP_TYPES:
            raise ValidationError(
                "employee_app_type must be one of: {}".format(
                    ", ".join(sorted(VALID_APP_TYPES))
                )
            )
        return value

    def _build_employee_password(self, mobile_number):
        if not mobile_number:
            return None
        mobile_number = str(mobile_number).strip()
        return base64.b64encode(mobile_number.encode("utf-8")).decode("utf-8")
