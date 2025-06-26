"""seed initial admin user

Revision ID: 05361dbdb067
Revises: 5b061988e514
Create Date: 2025-06-26 15:22:53.132699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from db.models import User
from schemas.enums import RoleEnum
from auth.utils import hash_password
# revision identifiers, used by Alembic.
revision: str = '05361dbdb067'
down_revision: Union[str, Sequence[str], None] = '5b061988e514'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Check if any users exist
    existing_user = session.query(User).first()
    if not existing_user:
        user = User(
            username="admin",
            email="admin@gmail.com",
            hashed_password=hash_password("admin123"),  # use a strong real password in production
            role=RoleEnum.admin
        )
        session.add(user)
        session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(User).filter_by(username="admin").delete()
    session.commit()
