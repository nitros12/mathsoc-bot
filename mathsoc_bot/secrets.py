import os

from dotenv import load_dotenv

load_dotenv()


def env_fail(var: str):
    """Warn about an empty env var."""
    print(f"Warning, missing env var: {var}")
    exit(1)


bot_client_token = os.getenv("BOT_TOKEN") or env_fail("BOT_TOKEN")

signing_secret = os.getenv("TOKEN_SECRET") or env_fail("TOKEN_SECRET")
