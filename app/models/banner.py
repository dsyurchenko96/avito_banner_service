import inspect
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class BannerBase(BaseModel):
    content: dict = Field(
        description="Содержимое баннера",
        example='{"title": "some_title", "text": "some_text", "url": "some_url"}',
    )

    class Config:
        orm_mode = True


class UserBannerGetResponse(BannerBase):
    pass


class BannerPostResponse(BaseModel):
    banner_id: int = Field(description="Идентификатор созданного баннера")

    class Config:
        orm_mode = True


class BannerPostRequest(BannerBase):
    tag_ids: List[int] = Field(description="Идентификаторы тэгов")
    feature_id: int = Field(description="Идентификатор фичи")
    is_active: bool = Field(description="Флаг активности баннера")


class AdminBannerGetResponse(BannerPostRequest):
    banner_id: int = Field(description="Идентификатор баннера")
    created_at: datetime = Field(description="Дата создания баннера")
    updated_at: datetime = Field(description="Дата обновления баннера")


class BannerPatchRequest(BannerBase):
    tag_ids: Optional[List[int]] = Field(description="Идентификаторы тэгов")
    feature_id: Optional[int] = Field(description="Идентификатор фичи")
    is_active: Optional[bool] = Field(description="Флаг активности баннера")
