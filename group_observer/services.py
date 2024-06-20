from fastapi import Depends, Query, APIRouter, Request
from aiogram.types import Message, Update
import json

from group_observer.app.bot import bot, dp
from group_observer.app.logger import logger


class RulesSaver:
    async def save_rule(self, request: Request):
        update = Update.model_validate(await request.json(), context={"bot": bot})
        logger.debug(json.dumps(update.dict(exclude_none=True), indent=4, ensure_ascii=False))
        a = await bot.get_business_connection(business_connection_id=update.business_message.business_connection_id)
        await dp.feed_update(bot, update)

