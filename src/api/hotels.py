import random
from fastapi import Query, Body, HTTPException, APIRouter

from sqlalchemy import insert, select

from src.database import async_session
from src.models.hotels import Hotels
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название Отеля"),
        location: str | None = Query(None, description="Место расположения Отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session() as session:
        query = select(Hotels)
        if title:
            query = query.where(Hotels.title.ilike(f"%{title}%"))
        if location:
            query = query.where(Hotels.location.ilike(f"%{location}%"))

        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        # Эта штука позволяет распечатать непосредственный запрос, который отправит
        # SQLAlchemy в БД, с подставленными туда значениями.
        # print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await session.execute(query)

        hotels = result.scalars().all()

        return hotels


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session() as session:
        add_hotel_stmt = insert(Hotels).values(**hotel_data.model_dump())

        # Эта штука позволяет распечатать непосредственный запрос, который отправит
        # SQLAlchemy в БД, с подставленными туда значениями.
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))

        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"success": True}


@router.put("/{hotel_id}")
async def update_hotel_put(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["cost$"] = hotel_data.cost
            break
    else:
        raise HTTPException(status_code=404)
    return {"success": True}


@router.patch("/{hotel_id}")
async def update_hotel_patch(
        hotel_id: int,
        hotel_data: HotelPatch,
):
    # Находим отель перед тем как патчить его
    global hotels
    hotel_to_patch = None
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel_to_patch = hotel
            break
    else:
        raise HTTPException(status_code=404)

    # Если дошли сюда, значит отель нашёлся по id и его можно патчить
    if hotel_data.title is not None:
        hotel_to_patch["title"] = hotel_data.title
    if hotel_data.cost is not None:
        hotel_to_patch["cost$"] = hotel_data.cost

    return {"success": True}


@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            break
    else:
        raise HTTPException(status_code=404)

    return {"success": True}
