from enum import Enum

from aiogram.filters import Command
from aiogram.types import Update, Message
from fastapi_utils.cbv import cbv
from fastapi import Depends, APIRouter

from group_observer.app.bot import dp, bot
from group_observer.app.dependencies import get_db_session
from group_observer.services import MessageHandlerService
from group_observer.common.db import MongoSession

router = APIRouter()


class CommandsEnum(str, Enum):
    add_rule = 'add_rule'
    rules_list = 'rules_list'


@cbv(router)
class OrderCBV:
    db_session: MongoSession = Depends(get_db_session)

    @router.post("/webhook")
    async def webhook(self, update: Update) -> None:
        await dp.feed_update(bot, update)


@dp.update()
async def _send_welcome1(message: Message) -> None:
    await message.answer("Welcome! Type any message and I'll echo it.")


@dp.message(Command('start'))
async def send_welcome(message: Message) -> None:
    await message.answer(
        'Привет! клёво, что обратился!\n'
        'Вот план действий:\n '
        '1. добавь меня в настройках телеграм в `Telegram Business`\n'
        f'2. введи команду `/{CommandsEnum.add_rule} id`, '
        'где id - это номер чата, откуда будешь отслеживать сообщения. '
        'Я буду пересылать сообщения оттуда в наш с тобой чат'
    )


@dp.message(Command(CommandsEnum.add_rule))
async def create_rule(message: Message) -> None:
    await MessageHandlerService().add_rule(message)
    await message.answer(
        'Создал правило: {rule}\n для обзора сообщений из чата: {chat}'
    )


@dp.business_message()
@dp.edited_business_message()
async def send_welcome3(message: Message) -> None:
    await message.reply('hey businesman')
