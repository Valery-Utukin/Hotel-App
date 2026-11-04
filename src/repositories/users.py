from src.repositories.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User


class UserRepository(BaseRepository):
    model = UsersORM
    schema = User