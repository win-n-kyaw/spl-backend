"""data types

Revision ID: fd2f98968de1
Revises: fc4d31ccbf46
Create Date: 2025-07-05 19:00:30.919790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd2f98968de1'
down_revision: Union[str, Sequence[str], None] = 'fc4d31ccbf46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('license_plate_requests', 'plate_image_url',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('license_plate_requests', 'plate_image_url',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=False)
    # ### end Alembic commands ###
