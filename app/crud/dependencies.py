from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy.schema import CreateTable, DropTable
from sqlalchemy import text


async def create_table(conn: AsyncConnection, table):
    stmt = str(CreateTable(table).compile(conn.engine))
    await conn.execute(text(stmt))


async def drop_table(conn: AsyncConnection, table):
    stmt = str(DropTable(table).compile(conn.engine))
    await conn.execute(text(stmt))
