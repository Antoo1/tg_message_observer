from fastapi import Depends, Query, APIRouter, Request
from aiogram.types import Update, Message
import json

from group_observer.app.bot import bot, dp
from group_observer.app.logger import logger


class MessageHandlerService:
    async def __call__(self, request: Request):
        payload = await request.json()
        update = Update.model_validate(payload, context={"bot": bot})
        logger.debug(json.dumps(update.dict(exclude_none=True), indent=4, ensure_ascii=False))
        if update.message:
            ...
        elif update.business_message:
            ...
        a = await bot.get_business_connection(business_connection_id=update.business_message.business_connection_id)
        await dp.feed_update(bot, update)

    async def add_rule(self, message: Message):
        ...

    async def show_rules_list(self, message: Message):
        ...
