"""Add created_at to bookings

Revision ID: 414e954d3397
Revises: 9a33cfccac2c
Create Date: 2026-11-25 22:26:37.336141

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "414e954d3397"
down_revision: Union[str, Sequence[str], None] = "9a33cfccac2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("bookings", "created_at")
