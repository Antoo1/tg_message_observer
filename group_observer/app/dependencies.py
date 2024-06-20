from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from group_observer.app.db import db_engine
from group_observer.common.db import setup_db_session


async def get_db_session() -> Generator[AsyncSession, None, None]:
    async with setup_db_session(db_engine)() as session:
        yield session
