from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_test, async_engine_test, async_engine
from app.db.models import Base, UserModel, CourseModel
from app.crud import (
    create_user,
    read_user_by_id,
    update_user_by_id,
    delete_user_by_id,
    count_all_users,
    delete_all_users,
)

import pytest


# username: str, email: str, hash_password: str
@pytest.fixture
def users():
    users_data = [
        ["Test1", "test1@gmail.com", "123"],
        ["Test2", "test2@gmail.com", "123"],
        ["Test3", "test3@gmail.com", "123"],
    ]
    return users_data


@pytest.fixture(scope="function")
async def clear_users(session):
    await delete_all_users(session)
    yield


@pytest.mark.usefixtures("clear_users")
class TestCrudUser:
    async def test_create_user(self, session: AsyncSession, users):
        for user in users:
            await create_user(session, user[0], user[1], user[2])

        count_users = await count_all_users(session)
        assert count_users == len(users)

    async def test_select_user_by_id(self, session: AsyncSession, users):
        user = await create_user(session, *users[0])

        current_user = await read_user_by_id(session, 1)
        assert current_user.username == user.username

    async def test_update_user_by_id(self, session: AsyncSession, users):
        user = await create_user(session, *users[0])
        updated_user = await update_user_by_id(
            session, 1, "Test1Update", "test1update@gmail.com", "1234"
        )
        refreshed_user = await read_user_by_id(session, 1)

        assert updated_user.username == refreshed_user.username
        assert updated_user.email == refreshed_user.email
        assert updated_user.hash_password == refreshed_user.hash_password

    async def test_delete_user_by_id(self, session: AsyncSession, users):
        user = await create_user(session, *users[0])
        await delete_user_by_id(session, 1)
        count_users = await count_all_users(session)
        assert count_users == 0
