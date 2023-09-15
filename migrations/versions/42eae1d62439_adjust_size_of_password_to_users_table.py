"""adjust size of password to users table

Revision ID: 42eae1d62439
Revises: 8029d8d91a6a
Create Date: 2023-09-12 02:30:27.555956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42eae1d62439'
down_revision: Union[str, None] = '8029d8d91a6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'password', type_=sa.String(128))


def downgrade() -> None:
    op.alter_column('users', 'password', type_=sa.String(32))

