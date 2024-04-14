from datetime import datetime

from psycopg2 import OperationalError
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True)
    feature_id = Column(Integer, ForeignKey("features.id"))
    content = Column(JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, default="some feature")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, default="some tag")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"))
    token = Column(String(255), nullable=False)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False)


class BannerTag(Base):
    __tablename__ = "banner_tags"

    banner_id = Column(Integer, ForeignKey("banners.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


# Create a PostgreSQL engine
engine = create_engine("postgresql://postgres:password123@db/avito_db", echo=True)
# Create the tables
try:
    Base.metadata.create_all(engine)
except OperationalError as err:
    print(err.pgerror)
    exit(1)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db = next(get_db())


def insert_data(db: SessionLocal):
    feature = Feature()
    db.add(feature)
    db.commit()
    banner = Banner(
        feature_id=1,
        content={"title": "some_title", "text": "some_text", "url": "some_url"},
        is_active=True,
    )
    db.add(banner)
    db.commit()


insert_data(db)
