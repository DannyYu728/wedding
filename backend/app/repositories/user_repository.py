from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import AbstractRepo
from app.core.exceptions import NotFoundError, DuplicateError

class SQLUserRepo(AbstractRepo[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, obj_in: UserCreate) -> User:
        data = obj_in.model_dump(exclude={"password"}, exclude_none=True)
        db_obj = User(**data)
        self.db.add(db_obj)
        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()
            raise DuplicateError("Email already registered") from e
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: UserUpdate) -> User:
        db_obj = await self.get(id)
        if not db_obj:
            raise NotFoundError(f"User with id {id} not found")
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: int) -> None:
        db_obj = await self.get(id)
        if not db_obj:
            raise NotFoundError(f"User with id {id} not found")
        await self.db.delete(db_obj)
        await self.db.commit()
