"""create user table

Revision ID: 8795b14ab812
Revises: 
Create Date: 2022-12-04 20:45:52.305515

"""
import uuid

from alembic import op
import sqlalchemy_utils as sau
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '8795b14ab812'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column(
            'uuid', UUID(as_uuid=True), primary_key=True, unique=True,
            default=uuid.uuid4().hex
        ),
        sa.Column('username', sa.String(30), unique=True, nullable=False),
        sa.Column('email', sau.EmailType, unique=True, nullable=False),
        sa.Column(
            'passwd', sau.PasswordType(schemes=['pbkdf2_sha512']),
            unique=False, nullable=False
        )
    )


def downgrade() -> None:
    pass
