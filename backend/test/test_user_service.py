import pytest
from types import SimpleNamespace
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import DuplicateError, NotFoundError

class FakeUserRepo:
    def __init__(self, existing=None, by_id=None):
        self._existing = existing or {}
        self._by_id = by_id or {}

    async def get_by_email(self, email: str):
        return self._existing.get(email)

    async def create(self, data: UserCreate):
        obj = SimpleNamespace(**data.model_dump(exclude_none=True))
        return obj

    async def get(self, id: int):
        return self._by_id.get(id)

    async def get_all(self, skip: int = 0, limit: int = 100):
        return list(self._by_id.values())

    async def update(self, id: int, data: UserUpdate):
        user = self._by_id.get(id)
        if not user:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(user, k, v)
        return user

    async def delete(self, id: int):
        if id in self._by_id:
            del self._by_id[id]

@pytest.mark.asyncio
async def test_register_duplicate():
    repo = FakeUserRepo(existing={"a@b.com": object()})
    svc = UserService(repo)
    payload = UserCreate(email="a@b.com", full_name="Test User", password="pass")
    with pytest.raises(DuplicateError):
        await svc.register(payload)

@pytest.mark.asyncio
async def test_register_success():
    repo = FakeUserRepo()
    svc = UserService(repo)
    payload = UserCreate(email="c@d.com", full_name="Charlie", password="x")
    user = await svc.register(payload)
    assert user.email == "c@d.com"

@pytest.mark.asyncio
async def test_get_not_found():
    repo = FakeUserRepo(by_id={})
    svc = UserService(repo)
    with pytest.raises(NotFoundError):
        await svc.get(123)

@pytest.mark.asyncio
async def test_get_all():
    u1 = SimpleNamespace(id=1)
    u2 = SimpleNamespace(id=2)
    repo = FakeUserRepo(by_id={1: u1, 2: u2})
    svc = UserService(repo)
    users = await svc.get_all()
    assert users == [u1, u2]

@pytest.mark.asyncio
async def test_update_and_delete_not_found():
    repo = FakeUserRepo(by_id={})
    svc = UserService(repo)
    with pytest.raises(NotFoundError):
        await svc.update(1, UserUpdate(
    full_name= None,
    appetizer_option_id=1,
    main_option_id=1,
    rsvp_confirmed=False,
    dietary_restrictions="shrimp"
))
    with pytest.raises(NotFoundError):
        await svc.delete(1)

