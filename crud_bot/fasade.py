from dataclasses import dataclass
from logging import Logger

from crud_bot.app.db import db_client
from crud_bot.rule_crud import RuleProvider
from crud_bot.dto import ChatRulesDTO


@dataclass
class DBFasade:
    logger: Logger

    async def get_rules_by_tg_id(self, tg_id: int) -> list[ChatRulesDTO]:
        async with await db_client.start_session() as db:
            try:
                return await RuleProvider(db, self.logger).get_rules_by_user_id(tg_id)
            except Exception as e:
                self.logger.error(f'error occurred:\n{e!r}')
                raise e
