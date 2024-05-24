import random
from hashlib import sha256

from faker import Faker
from sqlalchemy.orm import Session

from app.db.database import get_db, recreate_db
from app.models.tables import Admin, Banner, Feature, Tag, User


def generate_data(
    num_banners: int = 100,
    num_tags: int = 20,
    num_features: int = 5,
    db: Session = next(get_db()),
):
    fake = Faker()
    features = generate_features(num_features, fake, db)
    tags = generate_tags(num_tags, fake, db)
    generate_users(tags, db=db)
    generate_admins(db=db)
    avito_url = "https://www.avito.ru/banners/"
    for feature in features:
        available_tags = set(tags)
        for _ in range(random.randint(1, num_banners // num_features)):
            if not available_tags:
                break
            num_associated_tags = random.randint(1, min(num_tags, len(available_tags)))
            associated_tags = random.sample(list(available_tags), num_associated_tags)
            if not associated_tags:
                break
            available_tags -= set(associated_tags)
            content = {
                "title": fake.catch_phrase(),
                "text": fake.sentence(),
                "url": avito_url + fake.uri_path(),
            }
            is_active = random.choice([True, False])
            banner = Banner(feature_id=feature.id, content=content, is_active=is_active)
            banner.associated_tags = associated_tags
            db.add(banner)
    db.commit()


def generate_features(
    num_features: int, fake: Faker = Faker(), db: Session = next(get_db())
):
    features = []
    for _ in range(num_features):
        feature = Feature(description=fake.word())
        db.add(feature)
        features.append(feature)
    db.commit()
    return features


def generate_tags(num_tags: int, fake: Faker = Faker(), db: Session = next(get_db())):
    tags = []
    for _ in range(num_tags):
        tag = Tag(description=fake.word())
        db.add(tag)
        tags.append(tag)
    db.commit()
    return tags


def generate_users(tags: list[Tag], num_users: int = 10, db: Session = next(get_db())):
    for _ in range(num_users):
        user = User(tag_id=random.choice(tags).id, token=sha256(b"user").digest().hex())
        db.add(user)
    db.commit()


def generate_admins(num_admins: int = 1, db: Session = next(get_db())):
    for _ in range(num_admins):
        admin = Admin(token=sha256(b"admin").digest().hex())
        db.add(admin)
    db.commit()


if __name__ == "__main__":
    recreate_db()
    generate_data()
