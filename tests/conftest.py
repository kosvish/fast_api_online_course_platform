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


@pytest.fixture
def users_data():
    users_data = [
        {"username": "Test1", "email": "test1@gmail.com", "hash_password": "123"},
        {"username": "Test2", "email": "test2@gmail.com", "hash_password": "123"},
        {"username": "Test3", "email": "test3@gmail.com", "hash_password": "123"},
    ]
    return users_data


@pytest.fixture
def courses_data():
    courses_data = [
        {
            "title": "Django",
            "description": "Best Course for Django",
            "code_language": "Python",
            "creator_id": 1,
        },
        {
            "title": "FastAPI",
            "description": "Best Course for FastAPI",
            "code_language": "Python",
            "creator_id": 2,
        },
        {
            "title": "SQLAlchemy",
            "description": "Best Course for SQLAlchemy",
            "code_language": "Python",
            "creator_id": 3,
        },
    ]
    return courses_data
