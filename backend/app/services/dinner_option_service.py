from typing import List, Optional
from app.models.dinner_option import DinnerOption
from app.repositories.dinner_option_repository import SQLDinnerOptionRepo
from app.schemas.dinner_option import DinnerOptionOut

class DinnerOptionService:
    def __init__(self, repo: SQLDinnerOptionRepo):
        self.repo = repo

    async def get(self, option_id: int) -> Optional[DinnerOption]:
        return await self.repo.get(option_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[DinnerOption]:
        return await self.repo.get_all(skip, limit)

    async def create(self, payload: DinnerOptionOut) -> DinnerOption:
        return await self.repo.create(payload)

    async def update(self, option_id: int, payload: DinnerOptionOut) -> DinnerOption:
        return await self.repo.update(option_id, payload)

    async def delete(self, option_id: int) -> None:
        await self.repo.delete(option_id)