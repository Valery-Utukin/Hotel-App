from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    """
    Схема регистрации пользователя. Используется API-ручкой
    """
    nickname: str
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    """
    Схема для передачи репозиторию для добавления информации в БД
    """
    nickname: str
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    """
    Схема пользователя, для манипуляции в бизнес-логике. Никакого хэш-пароля из БД!
    """
    id: int
    nickname: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
