"""add salt to users table

Revision ID: 8029d8d91a6a
Revises: 
Create Date: 2023-09-12 01:39:27.804190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from models import User

# revision identifiers, used by Alembic.
revision: str = '8029d8d91a6a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('DELETE FROM users')
    op.add_column('users', User.salt)

def downgrade() -> None:
    op.drop_column('users', User.salt)
