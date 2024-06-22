from typing import Generator


from group_observer.app.db import db_client
from group_observer.common.db import MongoSession


async def get_db_session() -> Generator[MongoSession, None, None]:
    async with await db_client.start_session() as session:
        yield MongoSession(session)
