from crud_bot.app.logger import logger
from crud_bot.common.services import BaseServiceWithDB
from crud_bot.dto import ChatRulesDTO

import json


class CheckRuleService(BaseServiceWithDB):
    async def get_suitable_rule(self, message) -> ChatRulesDTO:
        logger.debug(json.dumps(message.dict(exclude_none=True), indent=4))
        # active_rules = await RuleProvider(self.db.db).get_active_rules()
