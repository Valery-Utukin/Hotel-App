from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(
        db: DBDep,
        data: UserRequestAdd,
):
    """
    <b>Регистрация нового пользователя.</b>
    <b>:param data:</b> Данные пользователя. Есть проверка на валидный email, но нет проверок для пароля.
    <b>:return:</b> JSON'чик с данными по созданному пользователю.
    """
    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(
        nickname=data.nickname,
        email=data.email,
        hashed_password=hashed_password,
    )

    new_user = await db.users.add(data=new_user_data)
    await db.commit()
    return {"success": True, "registered_user": new_user}


@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response,
):
    """
    Аутентификация пользователя. На данный момент для входа нужны все данные (никнейм, почта и пароль).
    TODO: Для входа можно использовать или никнейм+пароль, или почта+пароль.
    TODO: Не нужно передавать и почту и никнейм
    :param data: Данные для входа. Все данные (никнейм, почта и пароль)!
    :param response: Используется для добавления созданного токена в cookie-файлы
    :return:
    """
    # Проверяем что такой пользователь существует. ТОЛЬКО ПО EMAIL!
    user = await db.users.get_one_or_none(email=data.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

    # Вытаскиваем хэш пароля пользователя
    user_hash_password = await db.users.get_hashed_password_by_id(user_id=user.id)

    # Проверяем что хэш введенного пароля совпадает с хэшом в БД
    if AuthService().verify_password(data.password, user_hash_password):

        # Если всё совпало, то создаем новый access token (JWT) с информацией о пользователе
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
    """
    Эндпоинт только для авторизованных пользователей. Пока только возвращает данные пользователя.
    :param user_data:
    :return:
    """
    return {"data": user_data}


@router.post("/logout")
async def logout_user(
        user_data: UserIdDep,
        response: Response,
):
    """
    Выход пользователя из системы. Осуществляется простым удалением cookie-файлов.
    TODO:Токен авторизации не отзывается назад и не удаляется, нужно что-то придумать.
    :param user_data:
    :param response:
    :return:
    """
    response.delete_cookie("access_token")
    return {"data": f"User {user_data["user_data"]["user_nickname"]} logged out"}

