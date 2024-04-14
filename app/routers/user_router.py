from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.db.crud import get_banner
from app.db.database import get_db
from app.models.banner import UserBannerGetResponse
from app.utils.auth import is_user

router = APIRouter(
    responses={
        "400": {"description": "Некорректные данные"},
        "401": {"description": "Пользователь не авторизован"},
        "403": {"description": "Пользователь не имеет доступа"},
        "404": {"description": "Баннер не найден"},
        "500": {"description": "Внутренняя ошибка сервера"},
    },
)


@router.get(
    "/user_banner",
    response_model=UserBannerGetResponse,
    status_code=200,
)
async def get_user_banner(
    tag_id: PositiveInt,
    feature_id: PositiveInt,
    token: str,
    db: Session = Depends(get_db),
    use_last_revision: Optional[bool] = False,
) -> UserBannerGetResponse:
    """
    Получение баннера для пользователя на основе тэга и фичи
    """
    if not is_user(token):
        raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
    banner = get_banner(db, tag_id, feature_id)
    if banner is None:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    return banner
