"""Добваление колонки password для agent

Revision ID: 92cc80cfbc1a
Revises: 9055ce130b5b
Create Date: 2026-05-22 21:01:31.027333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92cc80cfbc1a'
down_revision: Union[str, Sequence[str], None] = '9055ce130b5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column('agent', sa.Column('password', sa.String(length=50), nullable=True))
     op.execute("UPDATE agent SET password = 'temporary_password' WHERE password IS NULL")
     op.alter_column('agent', 'password', nullable=False)

def downgrade() -> None:
     op.drop_column('agent', 'password')
