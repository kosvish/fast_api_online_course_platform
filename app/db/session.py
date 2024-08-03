from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from app.core import settings

async_engine = create_async_engine(settings.db_url, echo=False)

# создание асинхронной фабрики сессий:
async_session = async_sessionmaker(async_engine)


# Использование асинхронной сессии

