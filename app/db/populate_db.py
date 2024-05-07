from hashlib import sha256

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.tables import Admin, Banner, Feature, Tag, User


def insert_data(db: Session = next(get_db())):
    feature = Feature(description="new feature")
    tag = Tag()
    tag2 = Tag()
    user = User(tag_id=1, token=sha256(b"user").digest().hex())
    admin = Admin(token=sha256(b"admin").digest().hex())
    db.add_all([feature, tag, user, admin, tag2])
    db.commit()
    banner = Banner(
        feature_id=1,
        content={"title": "some_title", "text": "some_text", "url": "some_url"},
        is_active=True,
    )
    banner.associated_tags = [tag, tag2]
    db.add(banner)
    db.commit()


if __name__ == "__main__":
    insert_data()
