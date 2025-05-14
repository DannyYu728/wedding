from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.api.dependencies import get_db
from app.repositories.user_repository import SQLUserRepo
from app.services.user_service import UserService
from app.core.exceptions import NotFoundError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    svc = UserService(SQLUserRepo(db))
    try:
        user = await svc.get_by_email(form_data.username)
    except NotFoundError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    if not user or not svc.verify_password(user, form_data.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}
