from aiogram.types import Message
import json

from crud_bot.app.logger import logger
from crud_bot.common.services import BaseServiceWithDB
from crud_bot.rule_crud import RuleCreator, RuleProvider, RuleRemover
from crud_bot.dto import ChatRulesDTO, RuleDTO


class MessageCRUDService(BaseServiceWithDB):

    async def add_rule(self, rules: ChatRulesDTO) -> ChatRulesDTO:
        # logger.debug(json.dumps(message.dict(exclude_none=True), indent=4))
        await RuleCreator(self.db.db)(rules)
        return rules

    async def get_rules_list(self, message: Message) -> list[ChatRulesDTO]:
        return await RuleProvider(self.db.db).get_rules_by_user_id(message.from_user.id)

    async def delete_rule(self, message: Message):
        target_id = message.text.rsplit(' ')[1]
        await RuleRemover(self.db.db).remove_rule_by_target_id(
            user_id=int(message.from_user.id),
            target_id=int(target_id)
        )


def make_rules_from_message(message: Message) -> ChatRulesDTO:
    _, target_id, regexp, *forward_to = message.text.split('\n')
    if forward_to:
        forward_to = forward_to[0]
    regexp = regexp.split(' ')
    return ChatRulesDTO(
        target_chat_id=target_id,
        owner_chat_id=message.from_user.id,
        business_id=None,
        rules=[RuleDTO(regexp=r) for r in regexp],
        chat_name=None,
        chat_to_forward=forward_to or None
    )
