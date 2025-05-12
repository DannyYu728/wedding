from app.models.dinner_option import DinnerOption
from app.repositories.dinner_option_repository import SQLDinnerOptionRepo
from app.schemas.dinner_option import DinnerOptionOut
from app.core.exceptions import NotFoundError, DuplicateError

class DinnerOptionService:
    def __init__(self, repo: SQLDinnerOptionRepo):
        self.repo = repo

    async def get(self, option_id: int) -> DinnerOption:
        option = await self.repo.get(option_id)
        if not option:
            raise NotFoundError(f"Dinner option with id {option_id} not found")
        return option

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[DinnerOption]:
        return await self.repo.get_all(skip, limit)

    async def create(self, payload: DinnerOptionOut) -> DinnerOption:
        existing = await self.repo.get_by_name(payload.name)
        if existing:
            raise DuplicateError(f"Dinner option '{payload.name}' already exists")
        return await self.repo.create(payload)

    async def update(self, option_id: int, payload: DinnerOptionOut) -> DinnerOption:
        await self.get(option_id)
        return await self.repo.update(option_id, payload)

    async def delete(self, option_id: int) -> None:
        await self.get(option_id)
        await self.repo.delete(option_id)