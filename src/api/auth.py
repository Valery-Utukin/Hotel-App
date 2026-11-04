from fastapi import APIRouter
from passlib.context import CryptContext


from src.database import async_session
from src.repositories.users import UserRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)

    new_user_data = UserAdd(
        nickname=data.nickname,
        email=data.email,
        hashed_password=hashed_password,
    )

    async with async_session() as session:
        await UserRepository(session).add(data=new_user_data)
        await session.commit()
    return {"success": True}