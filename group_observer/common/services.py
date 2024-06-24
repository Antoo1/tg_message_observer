from dataclasses import dataclass

from motor.core import AgnosticDatabase

from group_observer.common.db import MongoSession


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
    db: AgnosticDatabase
