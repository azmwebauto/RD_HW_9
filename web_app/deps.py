from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from web_app import db


async def get_db() -> AsyncIterator[AsyncSession]:
    async with db.make_session() as session:
        yield session
