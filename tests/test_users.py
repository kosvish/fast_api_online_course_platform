from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_test, async_engine_test, async_engine
from app.db.models import Base, UserModel, CourseModel
from app.crud import (
    create_user,
    select_course_by_id,
    update_user_by_id,
    delete_user_by_id,
    count_all_users,
    delete_all_users, select_user_by_id,
)

import pytest


# username: str, email: str, hash_password: str


@pytest.fixture(scope="function")
async def setup_users(session, users_data):
    for user in users_data:
        await create_user(session, **user)

    yield
    await delete_all_users(session)


@pytest.mark.usefixtures("setup_users")
class TestCrudUser:

    async def test_select_user_by_id(self, session: AsyncSession, users_data):

        current_user = await select_user_by_id(session, 1)
        assert current_user.username == users_data[0]["username"]

    async def test_update_user_by_id(self, session: AsyncSession, users_data):
        updated_user = await update_user_by_id(
            session, 1, "Test1Update", "test1update@gmail.com", "1234"
        )
        refreshed_user = await select_user_by_id(session, 1)

        assert updated_user.username == refreshed_user.username
        assert updated_user.email == refreshed_user.email
        assert updated_user.hash_password == refreshed_user.hash_password

    async def test_delete_user_by_id(self, session: AsyncSession, users_data):
        await delete_user_by_id(session, 1)
        count_users = await count_all_users(session)
        assert count_users == len(users_data) - 1

    async def test_count_all_users(self, session, users_data):
        result = await count_all_users(session)
        assert result == len(users_data)
