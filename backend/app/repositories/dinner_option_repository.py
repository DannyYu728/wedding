from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.dinner_option import DinnerOption
from app.schemas.dinner_option import DinnerOptionOut
from app.repositories.base import AbstractRepo

class SQLDinnerOptionRepo(AbstractRepo[DinnerOption, DinnerOptionOut, DinnerOptionOut]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> Optional[DinnerOption]:
        result = await self.db.execute(select(DinnerOption).where(DinnerOption.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[DinnerOption]:
        result = await self.db.execute(select(DinnerOption).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: DinnerOptionOut) -> DinnerOption:
        db_obj = DinnerOption(**obj_in.dict())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: DinnerOptionOut) -> DinnerOption:
        db_obj = await self.get(id)
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> None:
        db_obj = await self.get(id)
        await self.db.delete(db_obj)
        await self.db.commit()
