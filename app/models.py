from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Organisation(TimestampMixin, db.Model):
    __tablename__ = "organisations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("organisations.id"), nullable=True)

    parent = db.relationship(
        "Organisation",
        remote_side=[id],
        backref=db.backref("children", lazy=True),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Designation(TimestampMixin, db.Model):
    __tablename__ = "designations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Employee(TimestampMixin, db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(64), nullable=False, unique=True, index=True)
    id_card_no = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True, index=True)
    name = db.Column(db.String(150), nullable=False)
    middle_name = db.Column(db.String(150), nullable=True)
    surname = db.Column(db.String(150), nullable=True)
    gender = db.Column(
        db.Enum("male", "female", "transgender", name="gender_enum"),
        nullable=True,
    )
    guardian_name = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    place_of_birth = db.Column(db.String(255), nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    education_level = db.Column(db.String(150), nullable=True)
    date_of_joining = db.Column(db.Date, nullable=True)
    designation = db.Column(
        db.Integer,
        db.ForeignKey("designations.id"),
        nullable=True,
        index=True,
    )
    category = db.Column(db.String(50), nullable=True)
    employment_type = db.Column(
        db.Enum("P", "T", "FT", "B", name="employment_type_enum"),
        nullable=True,
    )
    mobile_number = db.Column(db.String(20), nullable=False, unique=True, index=True)
    universal_account_number = db.Column(db.String(32), nullable=True)
    pan = db.Column(db.String(20), nullable=True)
    nominee = db.Column(db.Text, nullable=True)
    eps_nps = db.Column(db.String(50), nullable=True)
    family_details = db.Column(JSONB, nullable=True)
    posting_details = db.Column(JSONB, nullable=True)
    pay = db.Column(db.Numeric(12, 2), nullable=False, default=0.00)
    promotion = db.Column(db.Text, nullable=True)
    esic_insurance_no = db.Column(db.String(64), nullable=True)
    aadhaar_number = db.Column(db.String(20), nullable=True)
    bank_account_no = db.Column(db.String(64), nullable=True)
    bank_ifsc = db.Column(db.String(20), nullable=True)
    branch = db.Column(db.String(150), nullable=True)
    present_address = db.Column(db.Text, nullable=True)
    permanent_address = db.Column(db.Text, nullable=True)
    service_book_no = db.Column(db.String(64), nullable=True)
    date_of_exit = db.Column(db.Date, nullable=True)
    reason_for_exit = db.Column(db.Text, nullable=True)
    mark_of_identification = db.Column(db.Text, nullable=True)
    photo = db.Column(db.Text, nullable=True)
    specimen_signature_thumb_impression = db.Column(db.Text, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    organisation_id = db.Column(
        db.Integer,
        db.ForeignKey("organisations.id"),
        nullable=False,
        index=True,
    )
    employee_app_type = db.Column(
        db.Enum(
            "sadmin",
            "admin",
            "employee",
            "scanner",
            name="employee_app_type_enum",
        ),
        nullable=False,
        default="employee",
    )

    organisation = db.relationship("Organisation", backref=db.backref("employees", lazy=True))
    designation_ref = db.relationship(
        "Designation",
        backref=db.backref("employees", lazy=True),
        foreign_keys=[designation],
    )

    def to_dict(self):
        return {
            "id": self.id,
            "employee_code": self.employee_code,
            "id_card_no": self.id_card_no,
            "password": self.password,
            "name": self.name,
            "middle_name": self.middle_name,
            "surname": self.surname,
            "gender": self.gender,
            "guardian_name": self.guardian_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "place_of_birth": self.place_of_birth,
            "nationality": self.nationality,
            "education_level": self.education_level,
            "date_of_joining": self.date_of_joining.isoformat() if self.date_of_joining else None,
            "designation": self.designation,
            "category": self.category,
            "employment_type": self.employment_type,
            "email": self.email,
            "mobile_number": self.mobile_number,
            "universal_account_number": self.universal_account_number,
            "pan": self.pan,
            "nominee": self.nominee,
            "eps_nps": self.eps_nps,
            "family_details": self.family_details,
            "posting_details": self.posting_details,
            "pay": str(self.pay) if self.pay is not None else None,
            "promotion": self.promotion,
            "esic_insurance_no": self.esic_insurance_no,
            "aadhaar_number": self.aadhaar_number,
            "bank_account_no": self.bank_account_no,
            "bank_ifsc": self.bank_ifsc,
            "branch": self.branch,
            "present_address": self.present_address,
            "permanent_address": self.permanent_address,
            "service_book_no": self.service_book_no,
            "date_of_exit": self.date_of_exit.isoformat() if self.date_of_exit else None,
            "reason_for_exit": self.reason_for_exit,
            "mark_of_identification": self.mark_of_identification,
            "photo": self.photo,
            "specimen_signature_thumb_impression": self.specimen_signature_thumb_impression,
            "remarks": self.remarks,
            "organisation_id": self.organisation_id,
            "employee_app_type": self.employee_app_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
