import random
from fastapi import Query, HTTPException, APIRouter

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch


router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotel_names = [
    "Hilton", "Moscow Resort", "Mt.Olympus", "Hiawatha Resort",
    "Hotel1", "Hotel2", "Hotel3", "Hotel4",
]
hotels = [
    {"id": i + 1, "title": hotel_names[i], "cost$": random.randint(1, 9) * 100} for i in range(len(hotel_names))
]


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишка Отеля"),
        title: str | None = Query(None, description="Название Отеля"),
):
    hotels_ = []

    # Фильтруем все отели по id и title
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@router.post("")
async def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1, "title": hotel_data.title, "cost$": hotel_data.cost}
    )
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
