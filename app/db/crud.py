from typing import Optional

from sqlalchemy.orm import Session

from app.models.banner import (
    AdminBannerGetResponse,
    BannerPostRequest,
    BannerPostResponse,
    UserBannerGetResponse,
)
from app.models.tables import Banner, Feature, Tag, User


def get_banner(db: Session, feature_id: int, tag_id: int):
    response = (
        db.query(Banner)
        .filter(
            Banner.associated_tags.any(Tag.id == tag_id),
            Banner.feature_id == feature_id,
        )
        .first()
    )
    if response is None:
        return None
    return UserBannerGetResponse.from_orm(response)


def get_banners(
    db: Session,
    feature_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    skip: Optional[int] = 0,
    limit: Optional[int] = 1000,
):
    query = db.query(Banner)
    if feature_id is not None:
        query = query.filter(Banner.feature_id == feature_id)
    if tag_id is not None:
        query = query.filter(Banner.associated_tags.any(Tag.id == tag_id))
    results = query.offset(skip).limit(limit).all()

    if not results:
        return None

    return [AdminBannerGetResponse.from_orm(banner) for banner in results]


def create_banner(db: Session, banner: BannerPostRequest):
    db_banner = Banner(**banner.dict())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return BannerPostResponse.from_orm(db_banner)
