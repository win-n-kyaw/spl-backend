"""seed admin

Revision ID: 7b7321c92055
Revises: e885e928bcb5
Create Date: 2025-07-01 16:15:18.249484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import Session

from db.models import Admin
from schemas.enums import RoleEnum
from auth.utils import hash_password
import os
from dotenv import load_dotenv

load_dotenv()

SEED_USERNAME=os.getenv("SEED_USERNAME")
SEED_EMAIL=os.getenv("SEED_EMAIL")
SEED_PASSWORD=os.getenv("SEED_PASSWORD")

# revision identifiers, used by Alembic.
revision: str = '7b7321c92055'
down_revision: Union[str, Sequence[str], None] = 'e885e928bcb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    # Check if any users exist
    existing_user = session.query(Admin).first()
    if not existing_user:
        user = Admin(
            username=SEED_USERNAME,
            email=SEED_EMAIL,
            hashed_password=hash_password(
                SEED_PASSWORD #type: ignore
            ),  # use a strong real password in production
            role=RoleEnum.admin,
        )
        session.add(user)
        session.commit()
    pass


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(Admin).filter_by(username=SEED_USERNAME).delete()
    session.commit()
    pass
