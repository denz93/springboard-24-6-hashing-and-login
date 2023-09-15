"""add password_resets table

Revision ID: a42621d99001
Revises: 17780bdc3035
Create Date: 2023-09-13 20:48:25.110966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models import PasswordReset


# revision identifiers, used by Alembic.
revision: str = 'a42621d99001'
down_revision: Union[str, None] = '17780bdc3035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    PasswordReset.metadata.create_all(bind=op.get_bind(), tables=[PasswordReset.metadata.tables[PasswordReset.__tablename__]])

def downgrade() -> None:
    pass
