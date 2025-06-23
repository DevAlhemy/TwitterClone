from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base
from datetime import datetime
from typing import List


tweets_medias = Table(
    "tweets_medias",
    Base.metadata,
    Column("tweet_id", ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True),
    Column("media_id", ForeignKey("medias.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    api_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    tweets: Mapped[List["Tweet"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    liked_tweets: Mapped[List["Tweet"]] = relationship(
        secondary="likes",
        back_populates="liked_by",
        lazy="selectin"
    )

    followers: Mapped[List["User"]] = relationship(
        secondary="follows",
        primaryjoin="User.id == Follow.following_id",
        secondaryjoin="User.id == Follow.follower_id",
        back_populates="following",
        lazy="selectin"
    )

    following: Mapped[List["User"]] = relationship(
        secondary="follows",
        primaryjoin="User.id == Follow.follower_id",
        secondaryjoin="User.id == Follow.following_id",
        back_populates="followers",
        lazy="selectin"
    )


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="tweets")

    liked_by: Mapped[List["User"]] = relationship(
        secondary="likes",
        back_populates="liked_tweets",
        lazy="selectin"
    )

    attachments: Mapped[List["Media"]] = relationship(
        secondary=tweets_medias,
        back_populates="tweets",
        lazy="selectin"
    )


class Follow(Base):
    __tablename__ = "follows"
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    following_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )


class Like(Base):
    __tablename__ = "likes"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"),
        primary_key=True
    )


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

    tweets: Mapped[List["Tweet"]] = relationship(
        secondary=tweets_medias,
        back_populates="attachments",
        lazy="selectin"
    )
