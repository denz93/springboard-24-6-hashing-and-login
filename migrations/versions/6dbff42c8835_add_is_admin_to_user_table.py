"""add is_admin to user table

Revision ID: 6dbff42c8835
Revises: a42621d99001
Create Date: 2023-09-13 23:01:42.328140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dbff42c8835'
down_revision: Union[str, None] = 'a42621d99001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.execute('UPDATE users SET is_admin = False')
    op.alter_column('users', 'is_admin', nullable=True)


def downgrade() -> None:
    pass
