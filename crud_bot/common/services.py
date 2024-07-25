from dataclasses import dataclass
from logging import Logger

from motor.core import AgnosticDatabase

from crud_bot.common.db import MongoSession
from crud_bot.app.logger import logger


class BaseServiceWithDB:
    def __init__(self, db: MongoSession):
        self.db = db

    async def __aenter__(self):
        self.db.db_session.start_transaction()
        return self

    async def __aexit__(self, *args, **kwargs):
        if self.db.db_session.in_transaction:
            await self.db.db_session.commit_transaction()


@dataclass
class CRUDBase:
    _db: AgnosticDatabase
    logger: Logger = logger

    @property
    def db(self):
        return self._db.client.get_database()
