import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.main import app
from app.db.base import Base
from app.core.config import settings


pytestmark = pytest.mark.asyncio(loop_scope="session")

# Ensure HTTPX/AnyIO uses asyncio loop
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# Test database URL from .env.test
TEST_DATABASE_URL = settings.DATABASE_URL

# Async engine & session for tests
engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)   
#     yield loop
#     loop.close()
    
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    # Drop and recreate all tables once
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # Seed admin user
    from app.models.user import User
    async with TestingSessionLocal() as session:
        admin = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=pwd_context.hash("adminpass"),
            is_active=True,
            is_admin=True,
        )
        session.add(admin)
        await session.commit()
    yield
    # Dispose engine
    await engine.dispose()

@pytest.fixture(autouse=True)
def override_get_db(monkeypatch):
    # Override get_db dependency to use our test session
    async def get_db_override():
        async with TestingSessionLocal() as session:
            yield session
    monkeypatch.setattr(
        "app.api.dependencies.get_db",
        get_db_override,
    )
    yield

@pytest_asyncio.fixture
async def client():
    # ASGITransport so requests run in our app's loop
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client



