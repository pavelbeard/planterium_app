"""create bot_admin table

Revision ID: 5cf96ede9017
Revises: 8795b14ab812
Create Date: 2022-12-17 23:19:41.872052

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import BigInteger

# revision identifiers, used by Alembic.
revision = '5cf96ede9017'
down_revision = '8795b14ab812'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'bot_admin',
        sa.Column('user_id', BigInteger, primary_key=True, nullable=False)
    )


def downgrade() -> None:
    pass
