from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from web_app import config


def create_engine(db_url) -> AsyncEngine:
    return create_async_engine(db_url)


ENGINE = create_engine(config.DB_URI)


@asynccontextmanager
async def make_session(engine=ENGINE) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass
