from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel
from os import getenv
from dotenv import load_dotenv

load_dotenv()
BASE_DIR_PATH = Path(__file__).parent.parent
DB_PATH = BASE_DIR_PATH / "db.sqlite3"
DB_TEST_PATH = BASE_DIR_PATH / "db_test.sqlite3"

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")


class DbSettings(BaseModel):
    # url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    test_url: str = f"sqlite+aiosqlite:///{DB_TEST_PATH}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR_PATH / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR_PATH / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    # access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
