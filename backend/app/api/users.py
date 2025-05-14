from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import UserService
from app.core.exceptions import NotFoundError, DuplicateError
from app.api.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_user_service,
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        return await service.register(payload)
    except DuplicateError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=list[UserOut])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
    _admin=Depends(get_current_admin_user),
):
    return await service.get_all(skip, limit)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        return await service.get(user_id)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        return await service.update(user_id, payload)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        await service.delete(user_id)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

# endpoints for the authenticated guest
@router.get("/me", response_model=UserOut)
async def read_current_user(
    current_user=Depends(get_current_active_user)
):
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_current_user(
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_active_user),
):
    try:
        return await service.update(current_user.id, payload)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

