from typing import Optional

from sqlalchemy.orm import Session

from app.models.banner import UserBannerGetResponse
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
    limit: Optional[int] = 0,
):
    query = db.query(Banner)
    if feature_id is not None:
        query = query.filter(Banner.feature_id == feature_id)
    if tag_id is not None:
        query = query.filter(Banner.associated_tags.any(Tag.id == tag_id))
    if query is None:
        return None
    return [
        UserBannerGetResponse.from_orm(response)
        for response in query.offset(skip).limit(limit).all()
    ]


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
