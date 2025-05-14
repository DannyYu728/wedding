from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

from app.services     import UserService, DinnerOptionService, PlusOneService
from app.repositories import SQLUserRepo, SQLDinnerOptionRepo, SQLPlusOneRepo

from app.core.security import (
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
)


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    """
    Dependency that provides a UserService instance with its repository.
    """
    return UserService(SQLUserRepo(db))


def get_dinner_option_service(
    db: AsyncSession = Depends(get_db),
) -> DinnerOptionService:
    """
    Dependency that provides a DinnerOptionService instance with its repository.
    """
    return DinnerOptionService(SQLDinnerOptionRepo(db))


def get_plus_one_service(
    db: AsyncSession = Depends(get_db),
) -> PlusOneService:
    """
    Dependency that provides a PlusOneService instance with its repository.
    """
    return PlusOneService(SQLPlusOneRepo(db))
