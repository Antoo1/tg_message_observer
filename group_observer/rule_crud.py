from dataclasses import dataclass

from group_observer.common.services import CRUDBase
from group_observer.views.dto import ChatRulesDTO


class RuleCreator(CRUDBase):
    async def __call__(self, rule_dto: ChatRulesDTO) -> None:
        search_params = rule_dto.dict(include={'owner_chat_id', 'target_chat_id'})
        rules = await RuleProvider(self.db).get_rules(search_params)
        if len(rules) == 0:
            await self.db.rules.insert_one(rule_dto.dict())
        elif len(rules) == 1:
            rule_dto.enrich_from_existing(rules[0])
            await self.db.rules.update_one(
                filter=rule_dto.dict(include={'owner_chat_id', 'target_chat_id'}),
                update={'$set': rule_dto.dict()},
            )
        else:
            raise AssertionError('cannot be several records!!')


@dataclass
class RuleUpdater(CRUDBase):
    async def update_business_id(self, user_id: int, business_id: str):
        await self.db.rules.update(rules_dto.dict())


@dataclass
class RuleProvider(CRUDBase):
    async def get_rules_by_user_id(self, user_id: int) -> list[ChatRulesDTO]:
        field_name = 'owner_chat_id'
        assert field_name in ChatRulesDTO.model_fields
        return [ChatRulesDTO.model_validate(r)
                async for r in self.db.rules.find({field_name: user_id})]

    async def get_rules(self, search_kwargs: dict) -> list[ChatRulesDTO]:
        return [ChatRulesDTO.model_validate(r)
                async for r in self.db.rules.find(search_kwargs)]


@dataclass
class RuleRemover(CRUDBase):
    async def remove_rule_by_target_id(self, user_id: int, target_id: int):
        owner_chat_name = 'owner_chat_id'
        assert owner_chat_name in ChatRulesDTO.model_fields
        target_name = 'target_chat_id'
        assert target_name in ChatRulesDTO.model_fields
        return await self.db.rules.delete_one(
            {owner_chat_name: user_id, target_name: target_id}
        )
