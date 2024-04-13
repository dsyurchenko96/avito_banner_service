from typing import List
from typing import Optional

from fastapi import APIRouter

from app.models.banner import AdminBannerGetResponse
from app.models.banner import BannerPatchRequest
from app.models.banner import BannerPostRequest
from app.models.banner import BannerPostResponse


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
) -> List[AdminBannerGetResponse]:
    """
    Получение всех баннеров c фильтрацией по фиче и/или тегу
    """
    pass


@router.post(
    "/",
    response_model=BannerPostResponse,
)
def post_banner(token: str, body: BannerPostRequest) -> BannerPostResponse:
    """
    Создание нового баннера
    """
    pass


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
