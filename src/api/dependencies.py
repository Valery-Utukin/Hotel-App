from typing import Annotated
from fastapi import Depends, Query, Path, Request, HTTPException
from pydantic import BaseModel

from src.services.auth import AuthService


#  Зависимости для пагинации (отображение определенного кол-ва объектов на одну страницу)
class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(3, ge=3, lt=10)]


PaginationDep = Annotated[PaginationParams, Depends()]


#  Зависимости для аутентификации пользователя
def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Отсутствует токен")
    return token


def get_current_user_data(token: str = Depends(get_token)):
    data = AuthService().decode_token(token)
    return {"user_data": data}


UserIdDep = Annotated[dict, Depends(get_current_user_data)]


# Зависимости для параметров пути hotel_id и room_id. Используются в эндпоинтах для rooms
class HotelAndRoomParams(BaseModel):
    hotel_id: Annotated[int, Path(gt=0)]
    room_id: Annotated[int, Path(gt=0)]

HotelAndRoomDep = Annotated[HotelAndRoomParams, Depends()]