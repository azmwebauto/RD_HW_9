import asyncio

import pytest
import pytest_asyncio

from app import db
from app.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


DB_URI = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/test_db'
engine = db.create_engine(DB_URI)


@pytest_asyncio.fixture
async def create():
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(create):
    async with db.make_session(engine) as session:
        yield session
