from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.plus_one import PlusOneCreate, PlusOneOut, PlusOneUpdate
from app.services.plus_one_service import PlusOneService
from app.core.exceptions import NotFoundError, DuplicateError
from app.api.dependencies import (
    get_plus_one_service,
    get_current_active_user,
)

router = APIRouter(prefix="/users/me/plus-one", tags=["plus-one"])

@router.get("/", response_model=PlusOneOut)
async def read_my_plus_one(
    service: PlusOneService = Depends(get_plus_one_service),
    current_user=Depends(get_current_active_user),
):
    try:
        return await service.get_by_user(current_user.id)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=PlusOneOut, status_code=status.HTTP_201_CREATED)
async def add_my_plus_one(
    payload: PlusOneCreate,
    service: PlusOneService = Depends(get_plus_one_service),
    current_user=Depends(get_current_active_user),
):
    try:
        return await service.create(current_user.id, payload)
    except DuplicateError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))

@router.patch("/", response_model=PlusOneOut)
async def update_my_plus_one(
    payload: PlusOneUpdate,
    service: PlusOneService = Depends(get_plus_one_service),
    current_user=Depends(get_current_active_user),
):
    plus = await service.get_by_user(current_user.id)
    try:
        return await service.update(plus.id, payload)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_plus_one(
    service: PlusOneService = Depends(get_plus_one_service),
    current_user=Depends(get_current_active_user),
):
    plus = await service.get_by_user(current_user.id)
    try:
        await service.delete(plus.id)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))