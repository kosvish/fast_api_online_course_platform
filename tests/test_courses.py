from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_test, async_engine_test, async_engine
from app.db.models import Base, UserModel, CourseModel
from app.crud import (
    create_table,
    drop_table,
    delete_all_courses,
    count_courses,
    create_course,
    create_user,
    delete_all_users,
    select_course_by_id,
    select_user_by_id,
    update_course_by_id,
    delete_course_by_id,
    select_all_courses,
)

import pytest


# title: str,
# description: str,
# code_language: str,
# user_id: int = 1,


@pytest.fixture(scope="function")
async def setup_courses(session, courses_data):
    for course in courses_data:
        await create_course(session, **course)
    yield
    await delete_all_courses(session)


@pytest.mark.usefixtures("setup_courses")
class TestCrudCourse:
    async def test_select_course_by_id(self, session, courses_data):
        title, description, code_language, user_id = list(courses_data[0].values())
        fetched_course = await select_course_by_id(session, user_id)
        assert fetched_course.title == title
        assert fetched_course.description == description
        assert fetched_course.code_language == code_language
        assert fetched_course.user_id == user_id

    async def test_update_course_by_id(self, session, courses_data):
        title, description, code_language, user_id = list(courses_data[0].values())
        updated_course = await update_course_by_id(
            session,
            user_id,
            title="UpdatedTitle",
            description="UpdatedDesc",
            code_language="Java",
        )
        assert updated_course.title != title
        assert updated_course.description != description
        assert updated_course.code_language != code_language

    async def test_delete_course_by_id(self, session, courses_data):
        await delete_course_by_id(session, courses_data[0]["user_id"])
        len_result = await count_courses(session)
        assert len_result == len(courses_data) - 1

    async def test_count_all_courses(self, session, courses_data):
        result = await select_all_courses(session)
        assert len(result) == len(courses_data)
