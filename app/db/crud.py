from typing import Optional

from sqlalchemy.orm import Session

from app.models.banner import (
    AdminBannerGetResponse,
    BannerPatchRequest,
    BannerPostRequest,
    BannerPostResponse,
    UserBannerGetResponse,
)
from app.models.tables import Banner, Feature, Tag


def get_banner(db: Session, feature_id: int, tag_id: int):
    response = (
        db.query(Banner)
        .filter(
            Banner.associated_tags.any(Tag.id == tag_id),
            Banner.feature_id == feature_id,
        )
        .first()
    )
    if response is None or not response.is_active:
        return None
    return UserBannerGetResponse.model_validate(response)


def get_banners(
    db: Session,
    feature_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = 1000,
):
    query = db.query(Banner)
    if feature_id is not None:
        query = query.filter(Banner.feature_id == feature_id)
    if tag_id is not None:
        query = query.filter(Banner.associated_tags.any(Tag.id == tag_id))
    if not query.all():
        return None
    results = query.offset(offset).limit(limit).all()

    all_banners = []
    for banner_table in results:
        banner_dict = banner_table.__dict__
        banner_dict["tag_ids"] = [tag.id for tag in banner_table.associated_tags]
        banner_dict.pop("_sa_instance_state")
        banner_dict.pop("associated_tags")
        all_banners.append(AdminBannerGetResponse.model_validate(banner_dict))
    return all_banners


def create_banner(db: Session, banner: BannerPostRequest):
    if db.query(Feature).filter(Feature.id == banner.feature_id).first() is None:
        return None
    for tag_id in banner.tag_ids:
        if (
            db.query(Tag).filter(Tag.id == tag_id).first() is None
            or get_banner(db, banner.feature_id, tag_id) is not None
        ):
            return None
    db_banner = Banner(**banner.model_dump(exclude={"tag_ids"}))
    db_banner.associated_tags = [db.get(Tag, tag_id) for tag_id in banner.tag_ids]
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return BannerPostResponse.model_validate(db_banner)


def update_banner(db: Session, id: int, banner: BannerPatchRequest):
    query = db.query(Banner).filter(Banner.id == id)
    if query.first() is None:
        return None
    query.update(banner.model_dump(exclude_unset=True, exclude={"tag_ids"}))
    if banner.tag_ids is not None:
        query.first().associated_tags = [
            db.get(Tag, tag_id) for tag_id in banner.tag_ids
        ]
    db.add(query.first())
    db.commit()
    db.refresh(query.first())
    return {"description": "OK"}


def delete_banner(db: Session, id: int):
    banner = db.query(Banner).filter(Banner.id == id).first()
    if banner is None:
        return None

    banner.associated_tags.clear()
    db.delete(banner)
    db.commit()

    return {"description": "Баннер успешно удален"}
