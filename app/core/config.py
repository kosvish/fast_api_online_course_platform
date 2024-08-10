from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

BASE_DIR_PATH = Path(__file__).parent.parent
DB_PATH = BASE_DIR_PATH / "db.sqlite3"
DB_TEST_PATH = BASE_DIR_PATH / "db_test.sqlite3"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    test_url: str = f"sqlite+aiosqlite:///{DB_TEST_PATH}"
    echo: bool = True


class Settings(BaseSettings):
    db: DbSettings = DbSettings()


settings = Settings()
