from aiogram.types import Update
from fastapi_utils.cbv import cbv
from fastapi import Depends, APIRouter

from crud_bot.app.bot import bot
from crud_bot.app.dependencies import get_db_session
from crud_bot.common.db import MongoSession
from crud_bot.views.tg_views import dp

router = APIRouter()


@cbv(router)
class TelegramMessageCBV:
    db_session: MongoSession = Depends(get_db_session)

    @router.post('/webhook')
    async def webhook(self, update: Update) -> None:
        await dp.feed_update(bot, update, db_session=self.db_session)
