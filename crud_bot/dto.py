from typing import Callable
import re

from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator


class RuleDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    regexp: str

    def __hash__(self):
        return hash(self.regexp)

    def __eq__(self, other):
        if isinstance(other, RuleDTO):
            return self.regexp == other.regexp
        return False

    @property
    def pattern(self) -> Callable:
        return re.compile(self.regexp).search

    @field_validator('regexp')
    def is_valid_regexp(cls, v):
        try:
            re.compile(v)
        except re.error:
            raise ValueError(f'Invalid regexp: {v}')
        return v


class ChatRulesDTO(BaseModel):
    business_id: int | None
    owner_chat_id: int
    target_chat_id: int
    rules: list[RuleDTO] = Field(default_factory=set)
    chat_name: str | None
    chat_to_forward: int | None

    @property
    def key(self) -> tuple:
        return self.owner_chat_id, self.target_chat_id, self.chat_to_forward

    @model_validator(mode='after')
    def prevent_chat_to_forward_and_target_be_the_same(self):
        if (self.chat_to_forward or self.owner_chat_id) == self.target_chat_id:
            raise ValueError('target chat cannot be the same chat to forward')
        return self

    def enrich_from_existing(self, existing_dto: 'ChatRulesDTO'):
        self.business_id = self.business_id or existing_dto.business_id
        self.owner_chat_id = self.owner_chat_id or existing_dto.owner_chat_id
        self.target_chat_id = self.target_chat_id or existing_dto.target_chat_id
        self.chat_name = self.chat_name or existing_dto.chat_name
        self.chat_to_forward = self.chat_to_forward or existing_dto.chat_to_forward
        self.rules = list(set(self.rules).union(set(existing_dto.rules)))
