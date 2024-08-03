from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR_PATH}/db.sqlite3"
    db_echo: bool = True


settings = Settings()
