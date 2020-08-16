from cryptography.fernet import Fernet

from mathsoc_bot.secrets import email_encryption_key

fernet = Fernet(email_encryption_key)
