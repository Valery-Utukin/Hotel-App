from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User


class UserRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_hashed_password_by_id(self, user_id: int) -> str:
        """
        Возвращает хэш пароля пользователя с указанным id
        :param user_id: id пользователя в БД
        :return:
        """
        query = select(self.model.hashed_password).where(self.model.id == user_id)

        hashed_password = await self.session.execute(query)
        return hashed_password.scalars().one_or_none()