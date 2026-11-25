from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookingsORM
    schema = Booking
