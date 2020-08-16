from gino import Gino
from sqlalchemy import func
from sqlalchemy_utils import EncryptedType

from mathsoc_bot.secrets import email_encryption_key

db = Gino()

class User(db.Model):
    """Full users, that have a lancs email."""

    __tablename__ = "users"

    discord_id = db.Column(db.BigInteger(), primary_key=True)
    email = db.Column(EncryptedType(db.Text(), email_encryption_key), nullable=False)
    verified_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    _idx = db.Index("email_idx", "email", unique=True)
