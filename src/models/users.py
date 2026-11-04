from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import BaseOrm


class UsersORM(BaseOrm):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))