from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.db import CourseModel
from .db import get_async_session
from fastapi import Depends, HTTPException, status


async def get_course_by_id(
    course_id: int, session: AsyncSession = Depends(get_async_session)
) -> CourseModel:
    query = (
        select(CourseModel)
        .where(CourseModel.id == course_id)
        .order_by(CourseModel.id)
        .options(joinedload(CourseModel.creator))
    )
    course = await session.scalar(query)

    if course is None:
        raise HTTPException(
            detail="Course not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return course
