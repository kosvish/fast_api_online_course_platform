import pytest

from app.db import async_engine_test, async_session_test
from app.db.models import Base


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    print("Запускаюсь")
    # создаем тестовое соединение из пула соединений
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session():
    async with async_session_test() as s:
        yield s
