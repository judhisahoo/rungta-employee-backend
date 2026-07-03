"""add scanner employee app type

Revision ID: 0004_scanner_app_type
Revises: 0003_add_employee_id_card_no
Create Date: 2026-07-01
"""
from alembic import op


revision = "0004_scanner_app_type"
down_revision = "0003_add_employee_id_card_no"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TYPE employee_app_type_enum
        ADD VALUE IF NOT EXISTS 'scanner'
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE employees
        ALTER COLUMN employee_app_type TYPE text
        USING employee_app_type::text
        """
    )
    op.execute("DROP TYPE employee_app_type_enum")
    op.execute(
        """
        CREATE TYPE employee_app_type_enum
        AS ENUM ('sadmin', 'admin', 'employee')
        """
    )
    op.execute(
        """
        ALTER TABLE employees
        ALTER COLUMN employee_app_type TYPE employee_app_type_enum
        USING employee_app_type::employee_app_type_enum
        """
    )
