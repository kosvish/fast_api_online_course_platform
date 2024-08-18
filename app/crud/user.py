from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserModel


async def create_user(
    session: AsyncSession, username: str, email: str, hash_password: str
):
    user = UserModel(username=username, email=email, hash_password=hash_password)
    session.add(user)
    await session.commit()
    return user


async def select_all_users(session: AsyncSession) -> list[UserModel]:
    query = select(UserModel).order_by(UserModel.id)
    result = await session.scalars(query)
    return list(result)


async def select_user_by_id(session: AsyncSession, user_id: int) -> UserModel:
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


async def count_all_users(session: AsyncSession):
    query = select(UserModel).order_by(UserModel.id)
    result = await session.scalars(query)
    return len(list(result))


async def delete_all_users(session: AsyncSession):
    stmt = delete(UserModel)
    await session.execute(stmt)
    await session.commit()
