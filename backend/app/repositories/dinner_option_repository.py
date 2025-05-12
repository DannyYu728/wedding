from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.dinner_option import DinnerOption
from app.schemas.dinner_option import DinnerOptionOut
from app.repositories.base import AbstractRepo
from app.core.exceptions import NotFoundError, DuplicateError

class SQLDinnerOptionRepo(AbstractRepo[DinnerOption, DinnerOptionOut, DinnerOptionOut]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> Optional[DinnerOption]:
        result = await self.db.execute(select(DinnerOption).where(DinnerOption.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[DinnerOption]:
        result = await self.db.execute(select(DinnerOption).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_name(self, name: str) -> Optional[DinnerOption]:
        result = await self.db.execute(select(DinnerOption).where(DinnerOption.name == name))
        return result.scalars().first()

    async def create(self, obj_in: DinnerOptionOut) -> DinnerOption:
        try:
            db_obj = DinnerOption(**obj_in.dict())
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            raise DuplicateError(f"Dinner option '{obj_in.name}' already exists") from e

    async def update(self, id: int, obj_in: DinnerOptionOut) -> DinnerOption:
        db_obj = await self.get(id)
        if not db_obj:
            raise NotFoundError(f"Dinner option with id {id} not found")
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> None:
        db_obj = await self.get(id)
        if not db_obj:
            raise NotFoundError(f"Dinner option with id {id} not found")
        await self.db.delete(db_obj)
        await self.db.commit()