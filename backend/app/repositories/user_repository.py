from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import AbstractRepo

class SQLUserRepo(AbstractRepo[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: UserCreate) -> User:
        db_obj = User(**obj_in.dict(exclude={"password"}))
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: UserUpdate) -> User:
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
