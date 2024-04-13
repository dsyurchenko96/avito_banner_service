import inspect
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


def optional(*fields):
    """Decorator function used to modify a pydantic model's fields to all be optional.
    Alternatively, you can also pass the field names that should be made optional as arguments
    to the decorator.
    Taken from https://github.com/samuelcolvin/pydantic/issues/1223#issuecomment-775363074
    """

    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)

    return dec


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


@optional
class BannerPatchRequest(BannerPostRequest):
    pass
