from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

banner_tags = Table(
    'banner_tags',
    Base.metadata,
    Column('banner_id', Integer, ForeignKey('banners.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
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
    associated_feature = relationship("Feature", back_populates="associated_banners")
    associated_tags = relationship(
        "Tag",
        secondary="banner_tags",
        back_populates="associated_banners",
        cascade="all, delete",
    )

    def __repr__(self):
        return (
            f"Banner(id={self.id}, feature_id={self.feature_id},"
            f" content={self.content}, tags={self.associated_tags})"
        )


class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False, default="some feature")

    associated_banners = relationship("Banner", back_populates="associated_feature")


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False, default="some tag")

    associated_banners = relationship(
        "Banner", secondary=banner_tags, back_populates="associated_tags"
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'))

    tag = relationship("Tag")


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), nullable=False)
