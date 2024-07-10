from typing import List, Union, Optional
import telethon.tl.types

from pydantic import BaseModel as PydanticBaseModel


chat = Union[telethon.tl.types.Chat, telethon.tl.types.User]
chat_channels = Union[telethon.tl.types.Chat, telethon.tl.types.User, telethon.tl.types.Channel]


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class Subscription(BaseModel):
    group: str
    expr_rule: str
    forward_to: str


class ParsedSubscription(BaseModel):
    group: chat_channels
    expr_rule: str
    forward_to: chat


class User(BaseModel):
    tg_id: str
    subscriptions: List[Subscription]


class Users(BaseModel):
    users: List[User]
