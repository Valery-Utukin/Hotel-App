from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep
from src.database import async_session
from src.repositories.users import UserRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(
        nickname=data.nickname,
        email=data.email,
        hashed_password=hashed_password,
    )

    async with async_session() as session:
        await UserRepository(session).add(data=new_user_data)
        await session.commit()
    return {"success": True}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session() as session:
        # Проверяем что такой пользователь существует. ТОЛЬКО ПО EMAIL!
        user = await UserRepository(session).get_one_or_none(email=data.email)
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

        # Вытаскиваем хэш пароля пользователя
        user_hash_password = await UserRepository(session).get_hashed_password_by_id(user_id=user.id)

        # Проверяем что хэш введенного пароля совпадает с хэшом в БД
        if AuthService().verify_password(data.password, user_hash_password):
            access_token = AuthService().create_access_token(
                data={
                    "user_id": user.id,
                    "user_nickname": user.nickname
                }
            )

            # Добавляем access_token в cookie-файлы
            response.set_cookie("access_token", access_token)
            return {"access_token": access_token}
        else:
            raise HTTPException(status_code=401, detail="Неверный пароль")


@router.get("/only_auth")
async def only_auth(
        user_data: UserIdDep,
):
    return {"data": user_data}


@router.post("/logout")
async def logout_user(
        user_data: UserIdDep,
        response: Response,
):
    response.delete_cookie("access_token")
    return {"data": f"User {user_data["user_data"]["user_nickname"]} logged out"}

