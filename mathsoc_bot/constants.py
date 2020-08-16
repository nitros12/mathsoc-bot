import os

from dotenv import load_dotenv

load_dotenv()


def env_fail(var: str):
    """Warn about an empty env var."""
    print(f"Warning, missing env var: {var}")
    exit(1)

mathsoc_guild_id = int(os.getenv("GUILD_ID")) or env_fail("GUILD_ID")
verified_role_id = int(os.getenv("VERIFIED_ROLE_ID")) or env_fail("VERIFIED_ROLE_ID")

bot_log_channel_id = int(os.getenv("LOG_CHANNEL_ID")) or env_fail("LOG_CHANNEL_ID")

from_email_address = os.getenv("FROM_EMAIL_ADDRESS") or env_fail("FROM_EMAIL_ADDRESS")
