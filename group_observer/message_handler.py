from group_observer.app.logger import logger
from group_observer.common.services import BaseServiceWithDB
from group_observer.rule_crud import RuleProvider
from group_observer.views.dto import ChatRulesDTO

import json


class CheckRuleService(BaseServiceWithDB):
    async def get_suitable_rule(self, message) -> ChatRulesDTO:
        logger.debug(json.dumps(message.dict(exclude_none=True), indent=4))
        # active_rules = await RuleProvider(self.db.db).get_active_rules()
