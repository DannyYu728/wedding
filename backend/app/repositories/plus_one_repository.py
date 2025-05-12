from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.plus_one import PlusOne
from app.schemas.plus_one import PlusOneCreate, PlusOneUpdate
from app.repositories.base import AbstractRepo
from app.core.exceptions import NotFoundError, DuplicateError

class SQLPlusOneRepo(AbstractRepo[PlusOne, PlusOneCreate, PlusOneUpdate]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> Optional[PlusOne]:
        result = await self.db.execute(select(PlusOne).where(PlusOne.id == id))
        return result.scalars().first()

    async def get_by_user(self, user_id: int) -> Optional[PlusOne]:
        result = await self.db.execute(select(PlusOne).where(PlusOne.user_id == user_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[PlusOne]:
        result = await self.db.execute(select(PlusOne).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, user_id: int, data: PlusOneCreate) -> PlusOne:
        existing = await self.get_by_user(user_id)
        if existing:
            raise DuplicateError("A plus-one already exists for this user")
        db_obj = PlusOne(user_id=user_id, **data.dict())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: PlusOneUpdate) -> PlusOne:
        db_obj = await self.get(id)
        if not db_obj:
            raise NotFoundError(f"PlusOne with id {id} not found")
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> None:
        db_obj = await self.get(id)
        if not db_obj:
            raise NotFoundError(f"PlusOne with id {id} not found")
        await self.db.delete(db_obj)
        await self.db.commit()
