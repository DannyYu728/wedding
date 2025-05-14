from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.dinner_option import DinnerOptionOut
from app.services.dinner_option_service import DinnerOptionService
from app.core.exceptions import NotFoundError, DuplicateError
from app.api.dependencies import (
    get_dinner_option_service,
    get_current_active_user,
    get_current_admin_user,
)

router = APIRouter(prefix="/dinner-options", tags=["dinner-options"])

@router.get("/", response_model=list[DinnerOptionOut])
async def list_options(
    skip: int = 0,
    limit: int = 100,
    service: DinnerOptionService = Depends(get_dinner_option_service),
    user=Depends(get_current_active_user),
):
    return await service.get_all(skip, limit)

@router.get("/{option_id}", response_model=DinnerOptionOut)
async def get_option(
    option_id: int,
    service: DinnerOptionService = Depends(get_dinner_option_service),
    user=Depends(get_current_active_user),
):
    try:
        return await service.get(option_id)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=DinnerOptionOut, status_code=status.HTTP_201_CREATED)
async def create_option(
    payload: DinnerOptionOut,
    service: DinnerOptionService = Depends(get_dinner_option_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        return await service.create(payload)
    except DuplicateError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))

@router.patch("/{option_id}", response_model=DinnerOptionOut)
async def update_option(
    option_id: int,
    payload: DinnerOptionOut,
    service: DinnerOptionService = Depends(get_dinner_option_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        return await service.update(option_id, payload)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_option(
    option_id: int,
    service: DinnerOptionService = Depends(get_dinner_option_service),
    _admin=Depends(get_current_admin_user),
):
    try:
        await service.delete(option_id)
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))