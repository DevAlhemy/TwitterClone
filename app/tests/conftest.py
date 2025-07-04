from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core import SettingsConfigDict, Settings
from httpx import AsyncClient, ASGITransport
from db import get_db, Base, User
from dotenv import find_dotenv
from main import app
import pytest


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=find_dotenv(".env"))


test_settings = TestSettings()

TEST_DATABASE_URL = test_settings.ASYNC_DATABASE_URL

test_engine = create_async_engine(TEST_DATABASE_URL, future=True)

TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_engine.dispose()


@pytest.fixture(scope='session', autouse=True)
async def db():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope='session', autouse=True)
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture(scope='session', autouse=True)
async def test_user(db):
    user1 = User(name="test", api_key="test")
    user2 = User(name="admin", api_key="admin")
    db.add(user1)
    db.add(user2)
    await db.commit()
    await db.refresh(user1)
    await db.refresh(user2)
