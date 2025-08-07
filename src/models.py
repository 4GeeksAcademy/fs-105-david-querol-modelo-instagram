from flask_sqlalchemy import SQLAlchemy
import enum
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='author')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)

    user_from: Mapped[User] = db.relationship(
        'User', foreign_keys=[user_from_id])
    user_to: Mapped[User] = db.relationship('User', foreign_keys=[user_to_id])

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='posts')
    comment = db.relationship('Comment', back_populates='post', uselist=False)
    media = db.relationship('Media', back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(
        db.ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey('post.id'), unique=True, nullable=False)

    author = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comment', uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class MediaType(enum.Enum):
    IMAGE = enum.auto()
    VIDEO = enum.auto()
    AUDIO = enum.auto()


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    post_id: Mapped[int] = mapped_column(
        db.ForeignKey('post.id'), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)

    post = db.relationship('Post', back_populates='media')

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.name,
            "url": self.url
        }
