from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from app.db.crud import create_banner, delete_banner, get_banners, update_banner
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
    responses={
        "400": {"description": "Некорректные данные"},
        "401": {"description": "Пользователь не авторизован"},
        "403": {"description": "Пользователь не имеет доступа"},
        "500": {"description": "Внутренняя ошибка сервера"},
    },
)


@router.get("/", response_model=List[AdminBannerGetResponse], status_code=200)
def get_banner(
    token: str,
    feature_id: Optional[NonNegativeInt] = None,
    tag_id: Optional[NonNegativeInt] = None,
    limit: Optional[NonNegativeInt] = None,
    offset: Optional[NonNegativeInt] = None,
    db: Session = Depends(get_db),
):
    """
    Получение всех баннеров c фильтрацией по фиче и/или тегу
    """
    if not is_admin(token):
        if is_user(token):
            raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    banners = get_banners(db, feature_id, tag_id, offset, limit)
    if banners is None:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    return banners


@router.post("/", response_model=BannerPostResponse, status_code=201)
def post_banner(
    token: str,
    body: BannerPostRequest,
    db: Session = Depends(get_db),
):
    """
    Создание нового баннера
    """
    if not is_admin(token):
        if is_user(token):
            raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    response = create_banner(db, body)
    if response is None:
        raise HTTPException(status_code=400, detail="Некорректные данные")
    return response


@router.patch("/{id}", status_code=200)
def patch_banner_id(
    id: NonNegativeInt,
    token: str,
    body: BannerPatchRequest,
    db: Session = Depends(get_db),
):
    """
    Изменение баннера по идентификатору
    """
    if not is_admin(token):
        if is_user(token):
            raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    response = update_banner(db, id, body)
    if response is None:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    return response


@router.delete(
    "/{id}",
    status_code=204,
    responses={"204": {"description": "Баннер успешно удален"}},
)
def delete_banner_id(id: NonNegativeInt, token: str, db: Session = Depends(get_db)):
    """
    Удаление баннера по идентификатору
    """
    if not is_admin(token):
        if is_user(token):
            raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
        else:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    response = delete_banner(db, id)
    if response is None:
        raise HTTPException(status_code=404, detail="Баннер не найден")

    return response
