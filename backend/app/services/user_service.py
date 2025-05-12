from passlib.context import CryptContext
from typing import Optional, List
from app.models.user import User
from app.repositories.user_repository import SQLUserRepo
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundError, DuplicateError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repo: SQLUserRepo):
        self.repo = repo

    async def register(self, payload: UserCreate) -> User:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise DuplicateError("Email already registered")
        hashed = pwd_context.hash(payload.password)
        create_data = payload.copy(update={"hashed_password": hashed})
        return await self.repo.create(create_data)

    async def get(self, user_id: int) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")
        return user

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repo.get_all(skip, limit)

    async def update(self, user_id: int, payload: UserUpdate) -> User:
        await self.get(user_id)
        return await self.repo.update(user_id, payload)

    async def delete(self, user_id: int) -> None:
        await self.get(user_id)
        await self.repo.delete(user_id)
