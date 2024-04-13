from typing import Optional

from fastapi import APIRouter

from app.models.banner import UserBannerGetResponse


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
def get_user_banner(
    tag_id: int,
    feature_id: int,
    token: str,
    use_last_revision: Optional[bool] = False,
) -> UserBannerGetResponse:
    """
    Получение баннера для пользователя
    """
    pass
