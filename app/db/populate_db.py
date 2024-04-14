from hashlib import sha256

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.tables import Banner, Feature, Tag, User


def insert_data(db: Session = next(get_db())):
    feature = Feature()
    tag = Tag(description="a tag")
    user = User(tag_id=1, token=sha256(b"user").digest().hex())
    db.add_all([feature, tag, user])
    db.commit()
    banner = Banner(
        feature_id=1,
        content={"title": "some_title", "text": "some_text", "url": "some_url"},
        is_active=True,
    )
    banner.associated_tags.append(tag)
    db.add(banner)
    db.commit()


if __name__ == "__main__":
    insert_data()
