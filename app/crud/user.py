from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_async_session
from app.db.models import CourseModel, UserModel, CourseUserAssociation
import asyncio
from app.db import async_session


async def create_user(
    session: AsyncSession, username: str, email: str, hash_password: str
):
    user = UserModel(username=username, email=email, hash_password=hash_password)
    session.add(user)
    await session.commit()
    return user


async def read_user_by_id(session: AsyncSession, user_id: int) -> UserModel:
    query = select(UserModel).where(UserModel.id == user_id)
    user = await session.scalar(query)
    return user


async def update_user_by_id(
    session: AsyncSession, user_id: int, username: str, email: str, hash_password: str
) -> UserModel:
    query = select(UserModel).where(UserModel.id == user_id)
    user = await session.scalar(query)
    attrs = {"username": username, "email": email, "hash_password": hash_password}
    for attr, value in attrs.items():
        setattr(user, attr, value)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user_by_id(session: AsyncSession, user_id: int):
    stmt = delete(UserModel).where(UserModel.id == user_id)
    await session.execute(stmt)
    await session.commit()
    print("Удален")


async def main():
    async with async_session() as session:
        # user = await create_user(session, "Test", "test@gmail.com", "12345")
        # user = await read_user_by_id(session, 1)
        # user = await update_user_by_id(
        #     session, 1, "TestUpdate", "testupdate@gmail.com", "123456"
        # )
        # print(user.username)
        await delete_user_by_id(session, 1)

asyncio.run(main())
