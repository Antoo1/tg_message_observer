from typing import Iterable

from telethon import TelegramClient, events
from telethon.hints import EntityLike
from telethon.tl.custom import Message

from crud_bot.dto import RuleDTO, ChatRulesDTO
from .app.config import config
from .app.logger import logger
from .dto import ExistingRuleDTO, ExistingChatRulesDTO


class HandlerRegistryService:
    def __init__(self, tg_client: TelegramClient):
        self.client = tg_client
        self._existing_chat_rules_map: dict[tuple, ChatRulesDTO] = {}

    def update_handlers_if_differ(self, chat_rules: list[ChatRulesDTO]):
        for chat_rule in chat_rules:
            if existing_chat_rule := self._existing_chat_rules_map.get(chat_rule.key):
                rules_to_remove: set = existing_chat_rule.rules - set(chat_rule.rules)
                self._unregister_rules(rules=rules_to_remove, chats=chat_rule.target_chat_id)
                rules_to_create: set = set(chat_rule.rules) - existing_chat_rule.rules
                new_rules = self._register_rules(
                    rules=rules_to_create,
                    chats=chat_rule.target_chat_id,
                    forward_to=chat_rule.chat_to_forward or chat_rule.owner_chat_id,
                )
                existing_chat_rule.enrich_from_existing(chat_rule)
                existing_chat_rule.rules = (new_rules | set(existing_chat_rule.rules)) - rules_to_remove
            else:
                self.register_new_handlers([chat_rule])

    def register_new_handlers(self, chats: list[ChatRulesDTO]):
        for chat_rule in chats:
            rules = self._register_rules(
                rules=chat_rule.rules,
                chats=chat_rule.target_chat_id,
                forward_to=chat_rule.chat_to_forward or chat_rule.owner_chat_id,
            )
            new_created_rules = ExistingChatRulesDTO(
                **chat_rule.dict(exclude={'rules'}),
                rules=rules,
            )
            self._existing_chat_rules_map[chat_rule.key] = new_created_rules

    def _register_rules(
        self,
        rules: Iterable[RuleDTO],
        chats: EntityLike,
        forward_to=config.MY_ID
    ) -> set[ExistingRuleDTO]:
        """
            chats - username/peer/ID ...
        """
        created_rules = set()
        for rule in rules:
            handler = _make_forward_message_handler(forward_to=forward_to)
            self.client.add_event_handler(
                callback=handler,
                event=events.NewMessage(
                    chats=chats,
                    pattern=rule.pattern,
                )
            )
            logger.info(
                f'registered new rule: {rule!r}\nobserving_chat: {chats}\nforwads to: {forward_to}'
            )
            created_rules.add(ExistingRuleDTO(regexp=rule.regexp, handler=handler))
        return created_rules

    def _unregister_rules(self, rules: set[ExistingRuleDTO], chats):
        """
            chats - username/peer/ID ...
        """
        for rule in rules:
            self.client.remove_event_handler(
                callback=rule.handler,
                event=events.NewMessage(
                    chats=chats,
                    pattern=rule.regexp,
                )
            )
            logger.info(f'unregistered existing rule: {rule!r}')


def _make_forward_message_handler(forward_to: int):
    async def forward_message(event: Message):
        logger.info(f'Forwarding message {event.text} to {forward_to=}')
        await event.forward_to(forward_to)

    return forward_message
