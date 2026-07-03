"""add employee id card number

Revision ID: 0003_add_employee_id_card_no
Revises: b482a98600fa
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa


revision = "0003_add_employee_id_card_no"
down_revision = "b482a98600fa"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("employees", schema=None) as batch_op:
        batch_op.add_column(sa.Column("id_card_no", sa.String(length=64), nullable=True))

    op.execute(
        """
        UPDATE employees
        SET id_card_no = employee_code
        WHERE id_card_no IS NULL
        """
    )

    with op.batch_alter_table("employees", schema=None) as batch_op:
        batch_op.alter_column(
            "id_card_no",
            existing_type=sa.String(length=64),
            nullable=False,
        )
        batch_op.create_index(
            batch_op.f("ix_employees_id_card_no"),
            ["id_card_no"],
            unique=True,
        )


def downgrade():
    with op.batch_alter_table("employees", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_employees_id_card_no"))
        batch_op.drop_column("id_card_no")
