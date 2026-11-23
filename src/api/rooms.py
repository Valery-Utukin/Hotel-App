from fastapi import APIRouter, HTTPException, Path, Query, Response, Request
from typing import Annotated

from src.database import async_session
from src.schemas.rooms import RoomRequestAdd, RoomAdd, RoomPatch
from src.repositories.rooms import RoomRepository
from src.api.dependencies import HotelAndRoomDep, PaginationDep, DBDep



router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Номера"])


@router.get("")
async def get_rooms(
        pagination: PaginationDep,
        db: DBDep,
        hotel_id: Annotated[int, Path(gt=0)],
        title: str | None = Query(None, description="Название Номера"),
        min_price: int | None = Query(None, ge=0, description="Минимальная цена"),
        max_price: int | None = Query(None, ge=0, description="Максимальная цена"),
        min_quantity: int | None = Query(None, ge=0, description="Минимальное кол-во номеров"),
        max_quantity: int | None = Query(None, ge=0, description="Максимальное кол-во номеров"),
):
    """
    Возвращает номера из указанного отеля (hotel_id). Позволяет фильтровать результат по названию
    номера, мин. и макс. цене проживания и по мин. и макс. кол-ву доступных номеров.\n
    :param pagination:
    :param hotel_id: Айдишка отеля, в котором осуществляется поиск номеров\n
    :param title: Название номера
    :param min_price: Минимальная цена проживания за сутки\n
    :param max_price: Максимальная цена проживания за сутки\n
    :param min_quantity: Минимальное кол-во номеров в наличии\n
    :param max_quantity: Максимальное кол-во номеров в наличии\n
    :return: JSON'чик с данными по номерам. Если ничего не нашли, то вернется пустой список.
    """
    return await db.rooms.get_all(
        hotel_id=hotel_id,
        title=title,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )


@router.get("/{room_id}")
async def get_room_by_id(
        db: DBDep,
        hotel_and_room_id: HotelAndRoomDep,
):
    """
    Получить номер по его id и id отеля, в котором этот номер находится.\n
    :return: JSON с информацией о номере\n
    """
    room = await db.rooms.get_one_or_none(
        id=hotel_and_room_id.room_id,
        hotel_id=hotel_and_room_id.hotel_id,
    )
    return room


@router.post("/")
async def create_room(
        # Тут не используется HotelAndRoomDep, т.к. id комнаты ещё не известен.
        db: DBDep,
        room_data: RoomRequestAdd,
        hotel_id: Annotated[int, Path(gt=0)],
):
    """
    Создание номера в отеле с указанным id (hotel_id)\n
    :param room_data: Название, Описание, Цена, Кол-во таких номеров. Все поля обязательны!\n
    :param hotel_id: Айдишка отеля, в котором создается номер\n
    :return: JSON с информацией о созданном номере\n
    """

    # Создаем объект класса RoomAdd из переданных данных (класс RoomRequestAdd) и hotel_id
    room_to_add = RoomAdd(
        hotel_id=hotel_id,
        **room_data.model_dump(),
    )

    result = await db.rooms.add(data=room_to_add)
    await db.commit()
    return {"success": True, "created_data": result}


@router.put("/{room_id}")
async def update_room_put(
        db: DBDep,
        hotel_and_room_id: HotelAndRoomDep,
        room_data: RoomRequestAdd,
):
    """
    Обновление данных о номере. Все поля обязательны (PUT)!
    :param hotel_and_room_id:
    :param room_data:
    :return:
    """
    room = await db.rooms.get_one_or_none(
        id=hotel_and_room_id.room_id,
        hotel_id=hotel_and_room_id.hotel_id,
    )

    if room:
        updated_room = await db.rooms.update(
            data=room_data,
            id=room.id,
        )
        await db.commit()
        return {"success": True, "updated_data": updated_room}
    else:
        raise HTTPException(status_code=404, detail="Номер в отеле не найден")


@router.patch("/{room_id}")
async def update_room_patch(
        db: DBDep,
        hotel_and_room_id: HotelAndRoomDep,
        room_data: RoomPatch,
):
    """
    Частичное обновление данных о номере (PATCH).
    :param hotel_and_room_id:
    :param room_data:
    :return:
    """
    room = await db.rooms.get_one_or_none(
        id=hotel_and_room_id.room_id,
        hotel_id=hotel_and_room_id.hotel_id,
    )

    if room:
        updated_room = await db.rooms.update(
            data=room_data,
            id=room.id,
            is_patch=True,
        )
        await db.commit()
        return {"success": True, "updated_data": updated_room}
    else:
        raise HTTPException(status_code=404, detail="Номер в отеле не найден")


@router.delete("/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_and_room_id: HotelAndRoomDep,
):
    """
    Удаление информации о номере
    :param hotel_and_room_id:
    :return:
    """
    room = await db.rooms.get_one_or_none(
        id=hotel_and_room_id.room_id,
        hotel_id=hotel_and_room_id.hotel_id,
    )

    if room:
        deleted_room = await db.rooms.delete(
            id=room.id,
        )
        await db.commit()
        return {"success": True, "deleted_data": deleted_room}
    else:
        raise HTTPException(status_code=404, detail="Номер в отеле не найден")