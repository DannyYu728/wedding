from typing import List, Optional
from app.models.plus_one import PlusOne
from app.repositories.plus_one_repository import SQLPlusOneRepo
from app.schemas.plus_one import PlusOneCreate, PlusOneUpdate

class PlusOneService:
    def __init__(self, repo: SQLPlusOneRepo):
        self.repo = repo

    async def get(self, plus_one_id: int) -> Optional[PlusOne]:
        return await self.repo.get(plus_one_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[PlusOne]:
        return await self.repo.get_all(skip, limit)

    async def get_by_user(self, user_id: int) -> Optional[PlusOne]:
        return await self.repo.get_by_user(user_id)

    async def create(self, user_id: int, payload: PlusOneCreate) -> PlusOne:
        existing = await self.repo.get_by_user(user_id)
        if existing:
            raise ValueError("A plus-one already exists for this user")
        return await self.repo.create(user_id, payload)

    async def update(self, plus_one_id: int, payload: PlusOneUpdate) -> PlusOne:
        return await self.repo.update(plus_one_id, payload)

    async def delete(self, plus_one_id: int) -> None:
        await self.repo.delete(plus_one_id)
