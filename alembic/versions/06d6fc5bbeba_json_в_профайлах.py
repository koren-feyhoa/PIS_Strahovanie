"""json в профайлах

Revision ID: 06d6fc5bbeba
Revises: c35b31a883b5
Create Date: 2026-04-27 16:25:32.748531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06d6fc5bbeba'
down_revision: Union[str, Sequence[str], None] = 'c35b31a883b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('profile', sa.Column('type_document', sa.String, nullable=True))
    op.add_column('profile', sa.Column('info', sa.JSON, nullable=True))
    op.drop_column('profile', 'insurance_type')


def downgrade() -> None:
    op.add_column('profile', sa.Column('insurance_type', sa.String(30), nullable=True))

    op.drop_column('profile', 'type_document')
    op.drop_column('profile', 'info')
