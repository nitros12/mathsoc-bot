import datetime

from slug import slug
from gino import Gino
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import EncryptedType, observes
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

from luhack_bot.secrets import email_encryption_key

db = Gino()


class User(db.Model):
    __tablename__ = "users"

    discord_id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.Text(), nullable=False)
    email = db.Column(EncryptedType(db.Text(), email_encryption_key), nullable=False)


class Writeup(db.Model):
    __tablename__ = "writeups"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(None, db.ForeignKey("users.discord_id", ondelete="CASCADE"), nullable=False)
    author = relationship(User, backref=backref("writeups", passive_deletes=True))

    title = db.Column(db.Text(), nullable=False, unique=True)
    slug = db.Column(db.Text(), nullable=False, unique=True)

    tags = db.Column(ARRAY(db.Text()), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    creation_date = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    edit_date = db.Column(db.DateTime, server_default=func.now(), server_onupdate=func.now(), nullable=False)

    search_vector = db.Column(
        TSVectorType("title", "content", weights={"title": "A", "content": "B"})
    )

    _tags_idx = db.Index("writeups_tags_array_idx", "tags", postgresql_using="gin")

    @classmethod
    def create_auto(cls, *args, **kwargs):
        if "slug" not in kwargs:
            kwargs["slug"] = slug(kwargs["title"])
        return cls.create(*args, **kwargs)
    
    def update_auto(self, *args, **kwargs):
        if "slug" not in kwargs:
            kwargs["slug"] = slug(kwargs["title"])
        return self.update(*args, **kwargs)