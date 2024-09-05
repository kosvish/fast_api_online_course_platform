from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from app.core import settings

async_engine = create_async_engine(settings.db.url, echo=settings.db.echo)
async_engine_test = create_async_engine(settings.db.test_url, echo=True)

# создание асинхронной фабрики сессий:
async_session = async_sessionmaker(async_engine)
async_session_test = async_sessionmaker(async_engine_test)


# Использование асинхронной сессии

