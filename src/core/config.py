import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    TITLE: str = "URL shortener"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB: str = BASE_DIR + "/urls.db"
    SQLITE_DSN: str = Field("sqlite+aiosqlite:///" + DB, env="DATABASE_DSN")
    BLACK_LIST: set[str] = set()

    class Config:
        env_file = "../.env"


app_settings = Settings()
