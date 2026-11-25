from jwt import encode, decode, ExpiredSignatureError
from jwt.exceptions import DecodeError
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

from src.config import settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            data = decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return data
        except DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия токена истек")