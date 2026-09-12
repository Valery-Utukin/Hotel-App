from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# определяем абсолютный путь до корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        # pathlib позволяет формировать путь
        # с помощью оператора "/", аналогично os.path.join()
        env_file=BASE_DIR / ".env",
    )

settings = Settings()
