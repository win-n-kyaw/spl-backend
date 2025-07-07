"""add plate table

Revision ID: a7b003433d62
Revises: 9ede3f3aab82
Create Date: 2025-07-06 22:28:57.787816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b003433d62'
down_revision: Union[str, Sequence[str], None] = '9ede3f3aab82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.rename_table("user", "users")

    # Update foreign key reference
    op.drop_constraint("license_plates_user_id_fkey", "license_plates", type_="foreignkey")
    op.create_foreign_key("license_plates_user_id_fkey", "license_plates", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("license_plates_user_id_fkey", "license_plates", type_="foreignkey")
    op.create_foreign_key("license_plates_user_id_fkey", "license_plates", "user", ["user_id"], ["id"])
    op.rename_table("users", "user")

    # ### end Alembic commands ###
