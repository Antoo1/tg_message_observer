from typing import Callable

from crud_bot.dto import ChatRulesDTO, RuleDTO


class ExistingRuleDTO(RuleDTO):
    handler: Callable


class ExistingChatRulesDTO(ChatRulesDTO):
    rules: set[ExistingRuleDTO]

    def enrich_from_chat_rule(self, chat_rule):
        self.business_id = chat_rule.business_id or self.business_id
        self.owner_chat_id = chat_rule.owner_chat_id or self.owner_chat_id
        self.target_chat_id = chat_rule.target_chat_id or self.target_chat_id
        self.rules = chat_rule.rules or self.rules
        self.chat_name = chat_rule.chat_name or self.chat_name
        self.chat_to_forward = chat_rule.chat_to_forward or self.chat_to_forward
