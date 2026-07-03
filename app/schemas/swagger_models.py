from flask_restx import fields

from app.services.constants import (
    VALID_APP_TYPES,
    VALID_CATEGORIES,
    VALID_EMPLOYMENT_TYPES,
    VALID_GENDERS,
)


def create_error_model(namespace):
    return namespace.model(
        "Error",
        {"message": fields.String(required=True)},
    )


def create_organisation_model(namespace):
    return namespace.model(
        "Organisation",
        {
            "id": fields.Integer(readonly=True),
            "name": fields.String(required=True),
            "parent_id": fields.Integer,
            "created_at": fields.String(readonly=True),
            "updated_at": fields.String(readonly=True),
        },
    )


def create_designation_model(namespace):
    return namespace.model(
        "Designation",
        {
            "id": fields.Integer(readonly=True),
            "name": fields.String(required=True),
            "created_at": fields.String(readonly=True),
            "updated_at": fields.String(readonly=True),
        },
    )


def create_employee_model(namespace):
    return namespace.model(
        "Employee",
        {
            "id": fields.Integer(readonly=True),
            "employee_code": fields.String(
                required=True,
                description="Unique employee code.",
            ),
            "id_card_no": fields.String(
                required=True,
                description="Unique employee ID card number.",
            ),
            "password": fields.String(
                readonly=True,
                description=(
                    "Password is auto-generated from mobile number and stored "
                    "in base64 format."
                ),
            ),
            "name": fields.String(
                required=True,
                description="Full name of the employee.",
            ),
            "middle_name": fields.String(description="Middle name of the employee."),
            "surname": fields.String(description="Surname of the employee."),
            "gender": fields.String(
                enum=sorted(VALID_GENDERS),
                description="Gender of the employee.",
            ),
            "guardian_name": fields.String(
                description="Father's, mother's, or spouse's name."
            ),
            "date_of_birth": fields.String(description="Date in YYYY-MM-DD format."),
            "place_of_birth": fields.String(description="Place of birth."),
            "nationality": fields.String(description="Nationality of the employee."),
            "education_level": fields.String(
                description="Education level of the employee."
            ),
            "date_of_joining": fields.String(description="Date in YYYY-MM-DD format."),
            "designation": fields.Integer(description="Designation id."),
            "category": fields.String(enum=sorted(VALID_CATEGORIES)),
            "employment_type": fields.String(enum=sorted(VALID_EMPLOYMENT_TYPES)),
            "mobile_number": fields.String(
                required=True,
                description="Mobile number of the employee.",
            ),
            "email": fields.String(
                required=False,
                description="Email address of the employee.",
            ),
            "universal_account_number": fields.String(
                required=False,
                description="Universal Account Number (UAN) of the employee.",
            ),
            "pan": fields.String(description="PAN number of the employee."),
            "nominee": fields.String(description="Name of the nominee."),
            "eps_nps": fields.String(description="EPS/NPS number of the employee."),
            "family_details": fields.Raw,
            "posting_details": fields.Raw,
            "pay": fields.Float(required=True, description="Pay of the employee."),
            "promotion": fields.String(
                required=False,
                description="Promotion details.",
            ),
            "esic_insurance_no": fields.String(description="ESIC insurance number."),
            "aadhaar_number": fields.String(description="Aadhaar number of the employee."),
            "bank_account_no": fields.String(description="Bank account number."),
            "bank_ifsc": fields.String(description="Bank IFSC code."),
            "branch": fields.String,
            "present_address": fields.String,
            "permanent_address": fields.String,
            "service_book_no": fields.String,
            "date_of_exit": fields.String(description="Date in YYYY-MM-DD format."),
            "reason_for_exit": fields.String,
            "mark_of_identification": fields.String,
            "photo": fields.String(description="Photo URL, file path, or encoded value."),
            "specimen_signature_thumb_impression": fields.String,
            "remarks": fields.String,
            "organisation_id": fields.Integer(required=True),
            "employee_app_type": fields.String(enum=sorted(VALID_APP_TYPES)),
            "created_at": fields.String(readonly=True),
            "updated_at": fields.String(readonly=True),
        },
    )


def create_employee_search_model(namespace):
    return namespace.model(
        "EmployeeSearch",
        {
            "id_card_no": fields.String(
                required=True,
                example="JS312SC312",
                description="Unique employee ID card number.",
            ),
        },
    )


def create_generate_id_response_model(namespace):
    return namespace.model(
        "GenerateIdResponse",
        {
            "id_card_no": fields.String(
                required=True,
                example="A1B2C3D4E5F6G7H8",
            ),
        },
    )


def create_validate_id_card_no_model(namespace):
    return namespace.model(
        "ValidateIdCardNo",
        {
            "id_card_number": fields.String(
                required=True,
                example="JS312SC312",
                description="Employee ID card number to validate.",
            ),
        },
    )


def create_validate_id_card_no_response_model(namespace):
    return namespace.model(
        "ValidateIdCardNoResponse",
        {
            "exists": fields.Boolean(required=True),
            "message": fields.String(required=True),
        },
    )


def create_login_model(namespace):
    return namespace.model(
        "Login",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )


def create_register_model(namespace):
    return namespace.model(
        "Register",
        {
            "employee_code": fields.String(
                required=True,
                example="JS312SCANN",
                description="Unique employee code.",
            ),
            "id_card_no": fields.String(
                required=True,
                example="JS312SC312",
                description="Unique employee ID card number.",
            ),
            "name": fields.String(
                required=True,
                example="jscan",
                description="Full name of the employee.",
            ),
            "middle_name": fields.String(required=True, example="string"),
            "surname": fields.String(required=True, example="sahooscan"),
            "gender": fields.String(
                required=True,
                enum=sorted(VALID_GENDERS),
                example="male",
            ),
            "nationality": fields.String(required=True, example="indian"),
            "date_of_joining": fields.String(required=True, example="string"),
            "designation": fields.Integer(required=True, example=1),
            "category": fields.String(
                required=True,
                enum=sorted(VALID_CATEGORIES),
                example="Highly Skilled",
            ),
            "employment_type": fields.String(
                required=True,
                enum=sorted(VALID_EMPLOYMENT_TYPES),
                example="B",
            ),
            "mobile_number": fields.String(required=True, example="9861275404"),
            "email": fields.String(
                required=True,
                example="judhisahooscan@gmail.com",
            ),
            "pay": fields.Float(required=True, example=50000),
            "organisation_id": fields.Integer(required=True, example=7),
            "employee_app_type": fields.String(
                required=True,
                enum=sorted(VALID_APP_TYPES),
                example="scanner",
            ),
        },
    )


def create_login_success_model(namespace, employee_model):
    return namespace.model(
        "LoginSuccess",
        {
            "status": fields.Integer,
            "user": fields.Nested(employee_model),
            "access_token": fields.String,
            "refresh_token": fields.String,
        },
    )


def create_login_error_model(namespace):
    return namespace.model(
        "LoginError",
        {
            "Status": fields.Integer,
            "Message": fields.String,
        },
    )
