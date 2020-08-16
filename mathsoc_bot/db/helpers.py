from mathsoc_bot.db.models import db
from mathsoc_bot.secrets import db_url


async def init_db():
    await db.set_bind(db_url)
