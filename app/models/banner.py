from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BannerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserBannerGetResponse(BannerBase):
    content: dict = Field(
        description="Содержимое баннера",
        json_schema_extra={
            "example": '{"title": "some_title", "text": "some_text", "url": "some_url"}'
        },
    )


class BannerPostResponse(BannerBase):
    id: int = Field(description="Идентификатор созданного баннера")


class BannerPostRequest(BannerBase):
    content: dict = Field(
        description="Содержимое баннера",
        json_schema_extra={
            "example": '{"title": "some_title", "text": "some_text", "url": "some_url"}'
        },
    )
    tag_ids: List[int] = Field(description="Идентификаторы тэгов")
    feature_id: int = Field(description="Идентификатор фичи")
    is_active: bool = Field(description="Флаг активности баннера")


class AdminBannerGetResponse(BannerPostRequest):
    id: int = Field(description="Идентификатор баннера")
    created_at: datetime = Field(description="Дата создания баннера")
    updated_at: datetime = Field(description="Дата обновления баннера")


class BannerPatchRequest(BannerBase):
    content: Optional[dict] = Field(
        default=None,
        description="Содержимое баннера",
        json_schema_extra={
            "example": '{"title": "some_title", "text": "some_text", "url": "some_url"}'
        },
    )
    tag_ids: Optional[List[int]] = Field(
        default=None, description="Идентификаторы тэгов"
    )
    feature_id: Optional[int] = Field(default=None, description="Идентификатор фичи")
    is_active: Optional[bool] = Field(
        default=None, description="Флаг активности баннера"
    )
