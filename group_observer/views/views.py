from enum import Enum

from aiogram.filters import Command
from aiogram.types import Update, Message
from fastapi_utils.cbv import cbv
from fastapi import Depends, APIRouter

from group_observer.app.bot import dp, bot
from group_observer.app.dependencies import get_db_session
from group_observer.services import MessageCRUDService
from group_observer.common.db import MongoSession
from group_observer.views.dto import ChatRulesDTO

router = APIRouter()


@dp.business_message.outer_middleware()
async def get_user_session(
    handler,
    event,
    data,
):
    db_session: MongoSession = data['db_session']
    data = await db_session.db.rules.find_one({})
    # data = [r async for r in data]
    return handler(event, data)


class CommandsEnum(str, Enum):
    add_rule = 'add_rule'
    rules_list = 'rules_list'
    delete_rule = 'delete_rule'


@cbv(router)
class TelegramMessageCBV:
    db_session: MongoSession = Depends(get_db_session)

    @router.post('/webhook')
    async def webhook(self, update: Update) -> None:
        await dp.feed_update(bot, update, db_session=self.db_session)


def make_link():
    return 'https://t.me/{config.BOT_NAME}?start={CommandsEnum.add_rule.value}'


@dp.message(Command('start'))
async def send_welcome(message: Message) -> None:
    link = make_link()
    await message.answer(
        'Привет! клёво, что обратился!\n'
        'Вот план действий:\n '
        '1. добавь меня в настройках телеграм в `Telegram Business`\n'
        f'2. введи команду `<a {link}>/{CommandsEnum.add_rule.value}</a>`, '
        'где id - это номер чата, откуда будешь отслеживать сообщения. '
        'Я буду пересылать сообщения оттуда в наш с тобой чат'
    )


@dp.message(Command('help'))
async def send_help(message: Message) -> None:
    await message.answer(
        'список команд:\n'
        f'{CommandsEnum.add_rule.value} - создание новых правил\n'
        f'{CommandsEnum.rules_list.value} - получить список активных правил'
        f'{CommandsEnum.delete_rule.value} - удалить правило для группы'
    )


@dp.message(Command(CommandsEnum.add_rule))
@dp.edited_message(Command(CommandsEnum.add_rule))
async def create_rule(message: Message, db_session: MongoSession) -> None:
    if not message.from_user.is_premium:
        await message.answer(
            'у не премиум пользователя нет возможности добавить бота для обработки сообщений'
        )
        return
    rule = await MessageCRUDService(db_session).add_rule(message)
    await message.answer(
        'Создал правило:\n'
        f'{make_chat_rule_description(rule)}\n\n'
        'Если у тебя добавлен бот `Telegram Business` -> `ChatBots`, и выбраны чаты, '
        'то я буду присылать тебе оттуда оповещения'
    )


@dp.message(Command(CommandsEnum.rules_list))
async def get_rules(message: Message, db_session: MongoSession) -> None:
    rules = await MessageCRUDService(db_session).get_rules_list(message)
    rules_description = '\n\n'.join([make_chat_rule_description(r) for r in rules])
    await message.answer(
        f'Список активных правил: \n{rules_description}'
    )


@dp.message(Command(CommandsEnum.delete_rule))
async def delete_rules(message: Message, db_session: MongoSession) -> None:
    if len(args := message.text.split(' ')) != 2 or not args[1].isdigit():
        await message.reply(f'команда должна быть вида:\n/{CommandsEnum.delete_rule.value} `id`')
        return
    await MessageCRUDService(db_session).delete_rule(message)
    rules = await MessageCRUDService(db_session).get_rules_list(message)
    rules_description = '\n\n'.join([make_chat_rule_description(r) for r in rules])
    await message.answer(
        'Правило удалено\n'
        'Список активных правил: \n'
        f'{rules_description}'
    )


@dp.business_message()
@dp.edited_business_message()
async def send_welcome3(message: Message, db_session: MongoSession) -> None:
    await message.reply(f'hey businesman')


def make_chat_rule_description(rule: ChatRulesDTO) -> str:
    regexps = [r.regexp for r in rule.rules]
    return f'чат: {rule.chat_name or rule.target_chat_id}\nправила: {regexps}'
