from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class BookingRequestAdd(BaseModel):
    """
    Схема для добавления бронирования. Указывается только id номера и даты бронирования.
    Информация о цене и id отеля есть в схеме номера.
    Используется методами POST и PUT в api/rooms.py
    """
    room_id: int
    date_from: date
    date_to: date


class BookingAdd(BookingRequestAdd):
    """
    Схема для передачи репозиторию для добавления информации о бронировании в БД.
    Наследуется от BookingRequestAdd и добавляет только id пользователя и цену за сутки,
    нужные для таблицы БД.
    """
    user_id: int = Field(ge=1)
    price: int = Field(ge=1)


class Booking(BookingAdd):
    """
    Схема бронирования из БД. Атрибут total_cost (полная цена бронирования)
    вычисляется внутри ORM-модели - BookingORM, как hybrid_property.
    """
    id: int
    total_cost: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
