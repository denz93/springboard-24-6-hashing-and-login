"""restrict username ref as not nullable of feeback table

Revision ID: 17780bdc3035
Revises: 42eae1d62439
Create Date: 2023-09-12 16:39:07.796327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17780bdc3035'
down_revision: Union[str, None] = '42eae1d62439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('DELETE FROM feedbacks')
    op.alter_column('feedbacks', 'username', nullable=False)


def downgrade() -> None:
    pass
