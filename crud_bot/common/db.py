from motor.core import AgnosticClientSession, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReadPreference

from crud_bot.app.config import BaseConfig


def setup_db_engine(config: BaseConfig) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        config.ASYNC_DB_URL,
        read_preference=ReadPreference.PRIMARY
    )


class MongoSession:
    def __init__(self, session: AgnosticClientSession):
        self.db_session: AgnosticClientSession = session
        self.db: AgnosticDatabase = session.client.get_database()
