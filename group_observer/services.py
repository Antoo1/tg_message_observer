from aiogram.types import Message
import json

from group_observer.app.bot import bot
from group_observer.app.logger import logger
from group_observer.common.services import BaseServiceWithDB
from group_observer.rule_crud import RuleCreator, RuleUpdater, RuleProvider, RuleRemover
from group_observer.views.dto import ChatRulesDTO, ChatRulesDTO, RuleDTO


class MessageCRUDService(BaseServiceWithDB):

    async def add_rule(self, message: Message) -> ChatRulesDTO:
        logger.debug(json.dumps(message.dict(exclude_none=True), indent=4))
        rules = make_rules_from_message(message)
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

    async def update_business_connection(self, message: Message):
        business_connection = await bot.get_business_connection(
            business_connection_id=message.business_message.business_connection_id
        )
        await RuleUpdater(self.db.db).update_business_id(
            user_id=business_connection.user.id,
            business_id=business_connection.id,
        )


def make_rules_from_message(message: Message) -> ChatRulesDTO:
    _, target_id, regexp, *forward_to = message.text.split('\n')
    regexp = regexp.split(' ')
    return ChatRulesDTO(
        target_chat_id=target_id,
        owner_chat_id=message.from_user.id,
        business_id=None,
        rules=[RuleDTO(regexp=r) for r in regexp],
        chat_name=None,
        chat_to_forward=forward_to or None
    )
