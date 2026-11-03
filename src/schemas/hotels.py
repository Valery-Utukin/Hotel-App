from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    """
    Схема для добавления отеля. Используется методами POST и PUT в api/hotels.py
    """
    title: str
    location: str


class Hotel(HotelAdd):
    """
    Схема для получения объекта отеля из БД. Нужно для реализации Data Mapper'а
    """
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)