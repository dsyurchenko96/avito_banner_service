from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


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

    associated_tags = relationship(
        "Tag", secondary="banner_tags", back_populates="associated_banners"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, default="some tag")

    associated_banners = relationship(
        "Banner", secondary="banner_tags", back_populates="associated_tags"
    )


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False, default="some feature")


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
