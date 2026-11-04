"""add users table

Revision ID: 50c8e2b8895e
Revises: ef0eac9ab23d
Create Date: 2026-11-04 12:09:04.802165

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "50c8e2b8895e"
down_revision: Union[str, Sequence[str], None] = "ef0eac9ab23d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("nickname"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
