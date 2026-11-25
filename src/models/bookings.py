from datetime import date, datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import BaseOrm


class BookingsORM(BaseOrm):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]


    # TODO: Нужно почитать про этот декоратор!
    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days