from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_test, async_engine_test, async_engine
from app.db.models import Base, UserModel, CourseModel
from app.crud import (
    create_user,
    create_course,
    delete_all_users,
    delete_all_courses,
    select_all_courses_with_users_in_it,
    add_user_in_course,
)

import pytest


@pytest.fixture
async def create_users_courses(session, courses_data, users_data):
    for user in users_data:
        await create_user(session, **user)
    for course in courses_data:
        await create_course(session, **course)

    yield
    await delete_all_users(session)
    await delete_all_courses(session)


@pytest.mark.usefixtures("create_users_courses")
class TestCourseUserRelation:
    async def test_select_course_with_users_in_course(self, session, courses_data):
        result = await select_all_courses_with_users_in_it(session)
        assert len(courses_data) == len(result)

    async def test_check_users_in_course(self, session, users_data):
        pass
