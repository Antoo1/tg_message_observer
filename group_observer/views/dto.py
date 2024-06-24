from pydantic import BaseModel, Field, ConfigDict


class RuleDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    regexp: str


class ChatRulesDTO(BaseModel):
    business_id: int | None
    owner_chat_id: int
    target_chat_id: int
    rules: list[RuleDTO] = Field(default_factory=set)
    chat_name: str | None
    chat_to_forward: int | None

    def enrich_from_existing(self, existing_dto: 'ChatRulesDTO'):
        self.business_id = self.business_id or existing_dto.business_id
        self.owner_chat_id = self.owner_chat_id or existing_dto.owner_chat_id
        self.target_chat_id = self.target_chat_id or existing_dto.target_chat_id
        self.chat_name = self.chat_name or existing_dto.chat_name
        self.chat_to_forward = self.chat_to_forward or existing_dto.chat_to_forward
        self.rules = list(set(self.rules).union(set(existing_dto.rules)))
