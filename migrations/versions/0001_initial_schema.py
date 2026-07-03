"""initial organisation and employee schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-28
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    gender_enum = postgresql.ENUM(
        "male",
        "female",
        "transgender",
        name="gender_enum",
    )
    employment_type_enum = postgresql.ENUM(
        "P",
        "T",
        "FT",
        "B",
        name="employment_type_enum",
    )
    employee_app_type_enum = postgresql.ENUM(
        "sadmin",
        "admin",
        "employee",
        name="employee_app_type_enum",
    )

    gender_enum.create(op.get_bind(), checkfirst=True)
    employment_type_enum.create(op.get_bind(), checkfirst=True)
    employee_app_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "organisations",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "designations",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "employees",
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_code", sa.String(length=64), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("middle_name", sa.String(length=150), nullable=True),
        sa.Column("surname", sa.String(length=150), nullable=True),
        sa.Column(
            "gender",
            postgresql.ENUM(
                "male",
                "female",
                "transgender",
                name="gender_enum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("guardian_name", sa.String(length=255), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("place_of_birth", sa.String(length=255), nullable=True),
        sa.Column("nationality", sa.String(length=100), nullable=True),
        sa.Column("education_level", sa.String(length=150), nullable=True),
        sa.Column("date_of_joining", sa.Date(), nullable=True),
        sa.Column("designation", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=True),
        sa.Column(
            "employment_type",
            postgresql.ENUM(
                "P",
                "T",
                "FT",
                "B",
                name="employment_type_enum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("mobile_number", sa.String(length=20), nullable=False),
        sa.Column("universal_account_number", sa.String(length=32), nullable=True),
        sa.Column("pan", sa.String(length=20), nullable=True),
        sa.Column("nominee", sa.Text(), nullable=True),
        sa.Column("eps_nps", sa.String(length=50), nullable=True),
        sa.Column("family_details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("posting_details", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("pay", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("promotion", sa.Text(), nullable=True),
        sa.Column("esic_insurance_no", sa.String(length=64), nullable=True),
        sa.Column("aadhaar_number", sa.String(length=20), nullable=True),
        sa.Column("bank_account_no", sa.String(length=64), nullable=True),
        sa.Column("bank_ifsc", sa.String(length=20), nullable=True),
        sa.Column("branch", sa.String(length=150), nullable=True),
        sa.Column("present_address", sa.Text(), nullable=True),
        sa.Column("permanent_address", sa.Text(), nullable=True),
        sa.Column("service_book_no", sa.String(length=64), nullable=True),
        sa.Column("date_of_exit", sa.Date(), nullable=True),
        sa.Column("reason_for_exit", sa.Text(), nullable=True),
        sa.Column("mark_of_identification", sa.Text(), nullable=True),
        sa.Column("photo", sa.Text(), nullable=True),
        sa.Column("specimen_signature_thumb_impression", sa.Text(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("organisation_id", sa.Integer(), nullable=False),
        sa.Column(
            "employee_app_type",
            postgresql.ENUM(
                "sadmin",
                "admin",
                "employee",
                name="employee_app_type_enum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["designation"], ["designations.id"]),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_employees_designation"), "employees", ["designation"], unique=False)
    op.create_index(op.f("ix_employees_employee_code"), "employees", ["employee_code"], unique=True)
    op.create_index(op.f("ix_employees_organisation_id"), "employees", ["organisation_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_employees_organisation_id"), table_name="employees")
    op.drop_index(op.f("ix_employees_employee_code"), table_name="employees")
    op.drop_index(op.f("ix_employees_designation"), table_name="employees")
    op.drop_table("employees")
    op.drop_table("designations")
    op.drop_table("organisations")
    postgresql.ENUM(name="employee_app_type_enum").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="employment_type_enum").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="gender_enum").drop(op.get_bind(), checkfirst=True)
