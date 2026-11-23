from fastapi import Query, Body, HTTPException, APIRouter

from src.database import async_session
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.repositories.hotels import HotelRepository


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{hotel_id}")
async def get_hotel_by_id(
        db: DBDep,
        hotel_id: int,
):
    """
    Ручка по получение конкретного отеля по его id. Ничего необычного.\n
    <b>:param hotel_id:</b> Айдишка нужного отеля.\n
    :return: JSON'чик с данными по отелю. Либо, если не нашли его, возвращает 404
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel:
        return {"success": True, "data": hotel}
    return HTTPException(status_code=404)


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название Отеля"),
        location: str | None = Query(None, description="Место расположения Отеля"),
):
    """
    <b>Ручка на получение множества отелей по заданному названию или локации. Название или локация
    не обязательно должны быть точными. Они могут содержать лишь некоторые слова. Вернутся те сущности,
    которые содержат эти слова.</b>\n
    <b>:param pagination:</b> Определяет пагинацию для отелей. По сколько на странице (per_page)
    и какой номер страницы (page). Её типы и значения по-умолчанию задаются через dependency.\n
    <b>:param title:</b> Название Отеля\n
    <b>:param location:</b> Название локации Отеля (город, страна).\n
    <b>:return:</b> JSON'чик с данными по отелям. Если ничего не нашли, то вернется пустой список.
    """
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd,
):
    """
    <b>Ручка для создания новых отелей. Все параметры обязательны. Стандартный метод POST.</b>\n
    <b>:param hotel_data:</b> Данные об отеле: название (title) и местоположение (location).
    В качестве локации указывается город и страна (для простоты).\n
    <b>:return:</b> JSON'чик с данными по созданному отелю.
    """
    result = await db.hotels.add(data=hotel_data)
    await db.commit()
    return {"success": True, "created_data": result}


@router.put("/{hotel_id}")
async def update_hotel_put(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd,
):
    """
    <b>Ручка для обновления данных по отелям. Все параметры обязательны, т.к. это метод PUT.</b>\n
    <b>:param hotel_id:</b> Айдишка нужного отеля.\n
    <b>:param hotel_data:</b> Данные об отеле: название (title) и местоположение (location).
    В качестве локации указывается город и страна (для простоты).\n
    <b>:return:</b> JSON'чик с данными по обновленному отелю.
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)

    # Если нашелся отель с таким id, обновляем его и возвращаем данные
    if hotel:
        updated_hotel = await db.hotels.update(data=hotel_data, id=hotel_id)
        await db.commit()
        return {"success": True, "updated_data": updated_hotel}
    # В противном случае вернем 404
    return HTTPException(status_code=404)


@router.patch("/{hotel_id}")
async def update_hotel_patch(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatch,
):
    """
    <b>Ручка для частичного (PATCH) обновления данных по отелям.</b>\n
    <b>:param hotel_id:</b> Айдишка нужного отеля.\n
    <b>:param hotel_data:</b> Данные об отеле: название (title) и местоположение (location).
    В качестве локации указывается город и страна (для простоты).\n
    <b>:return:</b> JSON'чик с данными по обновленному отелю.
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)

    # Если нашелся отель с таким id, обновляем его и возвращаем данные
    if hotel:
        updated_hotel = await db.hotels.update(
            data=hotel_data,
            is_patch=True,
            id=hotel_id
        )
        await db.commit()
        return {"success": True, "updated_data": updated_hotel}
    # В противном случае вернем 404
    return HTTPException(status_code=404)


@router.delete("/{hotel_id}")
async def delete_hotel(
        db: DBDep,
        hotel_id: int,
):
    """
    <b>Ручка на удаление отеля. Удаляем по id. Всё просто.</b>\n
    <b>:param hotel_id:</b> Айдишка нужного отеля\n
    <b>:return:</b> Если отель удачно удалился, то возвращает JSON'чик с данными по удаленному отелю.\n
    Если отеля с таким id не найдено, то возвращает HTTPException 404.
    """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)

    # Если нашелся отель с таким id, то работаем с ним
    if hotel:
        result = await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {"success": True, "deleted data": result}
    # В противном случае вернем 404
    return HTTPException(status_code=404)


