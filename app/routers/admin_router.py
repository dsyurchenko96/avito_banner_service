from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud import create_banner, get_banners
from app.db.database import get_db
from app.models.banner import (
    AdminBannerGetResponse,
    BannerPatchRequest,
    BannerPostRequest,
    BannerPostResponse,
)
from app.utils.auth import is_admin, is_user

router = APIRouter(
    prefix="/banner",
)


@router.get("/", response_model=List[AdminBannerGetResponse], status_code=200)
def get_banner(
    token: str,
    feature_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[AdminBannerGetResponse]:
    """
    Получение всех баннеров c фильтрацией по фиче и/или тегу
    """
    if not is_admin(token):
        if is_user(token):
            raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    banners = get_banners(db, tag_id, feature_id)
    if banners is None:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    return banners


@router.post(
    "/",
    response_model=BannerPostResponse,
    status_code=201,
)
def post_banner(
    token: str,
    body: BannerPostRequest,
    db: Session = Depends(get_db),
) -> BannerPostResponse:
    """
    Создание нового баннера
    """
    if not is_admin(token):
        if is_user(token):
            raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    create_banner(db, body)


@router.patch(
    "/{id}",
)
def patch_banner_id(
    id: int, token: Optional[str] = None, body: BannerPatchRequest = ...
):
    """
    Обновление содержимого баннера
    """
    pass


@router.delete(
    "/{id}",
)
def delete_banner_id(id: int, token: str):
    """
    Удаление баннера по идентификатору
    """
    pass
