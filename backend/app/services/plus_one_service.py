from typing import List
from app.models.plus_one import PlusOne
from app.repositories.plus_one_repository import SQLPlusOneRepo
from app.schemas.plus_one import PlusOneCreate, PlusOneUpdate
from app.core.exceptions import NotFoundError

class PlusOneService:
    def __init__(self, repo: SQLPlusOneRepo):
        self.repo = repo

    async def get(self, plus_one_id: int) -> PlusOne:
        plus = await self.repo.get(plus_one_id)
        if not plus:
            raise NotFoundError(f"PlusOne with id {plus_one_id} not found")
        return plus

    async def get_by_user(self, user_id: int) -> PlusOne:
        plus = await self.repo.get_by_user(user_id)
        if not plus:
            raise NotFoundError(f"PlusOne for user {user_id} not found")
        return plus

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[PlusOne]:
        return await self.repo.get_all(skip, limit)

    async def create(self, user_id: int, payload: PlusOneCreate) -> PlusOne:
        return await self.repo.create(user_id, payload)

    async def update(self, plus_one_id: int, payload: PlusOneUpdate) -> PlusOne:
        await self.get(plus_one_id)
        return await self.repo.update(plus_one_id, payload)

    async def delete(self, plus_one_id: int) -> None:
        await self.get(plus_one_id)
        await self.repo.delete(plus_one_id)
