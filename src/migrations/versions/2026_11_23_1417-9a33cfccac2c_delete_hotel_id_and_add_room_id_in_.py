"""Delete hotel_id and Add room_id in bookings

Revision ID: 9a33cfccac2c
Revises: ae813db19cee
Create Date: 2026-11-23 14:17:34.296079

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9a33cfccac2c"
down_revision: Union[str, Sequence[str], None] = "ae813db19cee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("bookings", sa.Column("room_id", sa.Integer(), nullable=False))
    op.drop_constraint(op.f("bookings_hotel_id_fkey"), "bookings", type_="foreignkey")
    op.create_foreign_key(None, "bookings", "rooms", ["room_id"], ["id"])
    op.drop_column("bookings", "hotel_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "bookings",
        sa.Column("hotel_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    # WARNING: constraint name is None; this directive will fail as
    # rendered.  Add a name, or use a naming convention; see
    # https://alembic.sqlalchemy.org/en/latest/naming.html
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(
        op.f("bookings_hotel_id_fkey"), "bookings", "hotels", ["hotel_id"], ["id"]
    )
    op.drop_column("bookings", "room_id")
