from fastapi import Body, HTTPException, APIRouter

from src.api.dependencies import DBDep, UserIdDep, PaginationDep
from src.schemas.bookings import BookingRequestAdd, BookingAdd


router = APIRouter(prefix="/bookins", tags=["Бронирование номеров"])


@router.get("")
async def get_bookings(
        db: DBDep,
        pagination: PaginationDep,
):
    """
    Получение всех бронирований.
    :param db:
    :param pagination:
    :return: Все бронирования в соответствии с пагинацией.
    """
    bookings = await db.bookings.get_all(
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )
    return bookings


@router.get("/me")
async def get_bookings_me(
        db: DBDep,
        user_data: UserIdDep,
        pagination: PaginationDep,
):
    """
    Получение бронирований пользователя. Требуется Аутентификация!
    :param db:
    :param user_data:
    :param pagination:
    :return: Все бронирования пользователя в соответствии с пагинацией.
    """
    bookings = await db.bookings.get_all(
        user_id=user_data["user_data"]["user_id"],
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )
    return bookings


@router.post("")
async def create_booking(
        db: DBDep,
        user_data: UserIdDep,
        booking_data: BookingRequestAdd = Body(),
):
    """
    Создание бронирования номера пользователем. Требуется Аутентификация!
    :param db:
    :param user_data: Зависимость из которой получаем user_id. Эта зависимость отвечает
    за аутентификацию пользователя.
    :param booking_data:
    :return:
    """
    # Ищем в БД номер, чтобы взять у него цену за сутки
    # Если комнаты нет, то возвращаем исключение 404
    room_info = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room_info is None:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    # Создаем объект бронирования, который передадим в БД
    booking_to_add = BookingAdd(
        user_id=user_data["user_data"]["user_id"],
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room_info.price,
    )

    # Создаем запись в БД и возвращаем информацию по созданному бронированию
    created_booking = await db.bookings.add(data=booking_to_add)
    await db.commit()

    return {"success": True, "created_booking": created_booking}
