import os

from dotenv import load_dotenv

load_dotenv()


def env_fail(var: str):
    """Warn about an empty env var."""
    print(f"Warning, missing env var: {var}")
    exit(1)


db_url = os.getenv("DB_URL")

sendgrid_token = os.getenv("SENDGRID_TOKEN") or env_fail("SENDGRID_TOKEN")

bot_client_token = os.getenv("BOT_TOKEN") or env_fail("BOT_TOKEN")

email_encryption_key = os.getenv("EMAIL_KEY") or env_fail("EMAIL_KEY")

signing_secret = os.getenv("TOKEN_SECRET") or env_fail("TOKEN_SECRET")
