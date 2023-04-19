import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    title: str = "URL shortener"
    host: str = "127.0.0.1"
    port: int = 8000
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db: str = base_dir + "/urls.db"
    sqlite_dsn: str = Field("sqlite+aiosqlite:///" + db, env="DATABASE_DSN")
    black_list: set[str] = set()

    class Config:
        env_file = "../.env"


app_settings = Settings()
