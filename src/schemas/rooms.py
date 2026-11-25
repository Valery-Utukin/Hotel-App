from pydantic import BaseModel, Field, ConfigDict


class RoomRequestAdd(BaseModel):
    """
    Схема для добавления номера. Базовая информация о номере без hotel_id, к которому он относится.
    Используется методами POST и PUT в api/rooms.py
    """
    title: str  # Название (стандарт, семейный, люкс, тяжелый-люкс)
    description: str | None  = Field(None)  # Описание
    price: int = Field(gt=0)  # Цена проживания за сутки. Простая валидация на отрицательные числа - gt=0
    quantity: int = Field(gt=0) # Кол-во таких номеров. Простая валидация на отрицательные числа - gt=0


class RoomAdd(RoomRequestAdd):
    """
    Схема для передачи репозиторию для добавления информации о номере в БД.
    Наследуется от RoomRequestAdd и добавляет только id отеля, нужный для таблицы БД.
    """
    hotel_id: int = Field(ge=1)  # id отеля с простой валидацией на "больше нуля" - ge=1


class Room(RoomAdd):
    """
    Схема номера из БД. Содержит всю информацию о номере.
    Самый младший класс в цепочке наследования:
    BaseModel -> RoomRequestAdd -> RoomAdd -> Room
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPatch(BaseModel):
    title: str | None = Field(None) # Название (стандарт, семейный, люкс, тяжелый-люкс)
    description: str | None = Field(None)  # Описание
    price: int | None = Field(None, gt=0)  # Цена проживания за сутки. Простая валидация на отрицательные числа - gt=0
    quantity: int | None = Field(None, gt=0)  # Кол-во таких номеров. Простая валидация на отрицательные числа - gt=0
