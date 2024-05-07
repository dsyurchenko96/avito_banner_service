from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BannerBase(BaseModel):
    content: dict = Field(
        description="Содержимое баннера",
        example='{"title": "some_title", "text": "some_text", "url": "some_url"}',
    )

    class Config:
        from_attributes = True


class UserBannerGetResponse(BannerBase):
    pass


class BannerPostResponse(BaseModel):
    id: int = Field(description="Идентификатор созданного баннера")

    class Config:
        from_attributes = True


class BannerPostRequest(BannerBase):
    tag_ids: List[int] = Field(description="Идентификаторы тэгов")
    feature_id: int = Field(description="Идентификатор фичи")
    is_active: bool = Field(description="Флаг активности баннера")


class AdminBannerGetResponse(BannerPostRequest):
    id: int = Field(description="Идентификатор баннера")
    created_at: datetime = Field(description="Дата создания баннера")
    updated_at: datetime = Field(description="Дата обновления баннера")


class BannerPatchRequest(BaseModel):
    content: Optional[dict] = Field(
        default=None,
        description="Содержимое баннера",
        example='{"title": "some_title", "text": "some_text", "url": "some_url"}',
    )
    tag_ids: Optional[List[int]] = Field(
        default=None, description="Идентификаторы тэгов"
    )
    feature_id: Optional[int] = Field(default=None, description="Идентификатор фичи")
    is_active: Optional[bool] = Field(
        default=None, description="Флаг активности баннера"
    )
