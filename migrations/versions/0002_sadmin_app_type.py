"""use sadmin employee app type

Revision ID: 0002_sadmin_app_type
Revises: 0001_initial_schema
Create Date: 2026-06-28
"""
from alembic import op


revision = "0002_sadmin_app_type"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_enum e
                JOIN pg_type t ON t.oid = e.enumtypid
                WHERE t.typname = 'employee_app_type_enum'
                  AND e.enumlabel = 'Super Admin'
            ) THEN
                ALTER TYPE employee_app_type_enum RENAME VALUE 'Super Admin' TO 'sadmin';
            END IF;
        END $$;
        """
    )


def downgrade():
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_enum e
                JOIN pg_type t ON t.oid = e.enumtypid
                WHERE t.typname = 'employee_app_type_enum'
                  AND e.enumlabel = 'sadmin'
            ) THEN
                ALTER TYPE employee_app_type_enum RENAME VALUE 'sadmin' TO 'Super Admin';
            END IF;
        END $$;
        """
    )
