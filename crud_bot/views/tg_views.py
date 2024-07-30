from enum import Enum

from aiogram import F
from aiogram.enums import ParseMode
from aiogram.filters import Command, ExceptionTypeFilter

from aiogram.types import Message, ErrorEvent

from crud_bot.app.bot import dp
from crud_bot.app.config import config
from crud_bot.app.exceptions import AppError
from crud_bot.app.logger import logger
from crud_bot.common.db import MongoSession
from crud_bot.dto import ChatRulesDTO
from crud_bot.services import MessageCRUDService, make_rules_from_message


class CommandsEnum(str, Enum):
    add_rule = 'add_rule'
    rules_list = 'rules_list'
    delete_rule = 'delete_rule'


def make_link():
    return f'https://t.me/{config.BOT_NAME}?{CommandsEnum.add_rule.value}'


def make_example_with_description(message: Message):
    return (
        '```\n'
        f'/{CommandsEnum.add_rule.value}\n'
        f'target_chat_id\n'
        'regexp\n```\n'
        'где: \n'
        'target_chat_id - id группы чата, для отслеживания сообщений\n'
        'regexp - правила по которым будут присылаться сообщения\n'
        # f'{message.from_user.id} - это твой id,  '
    )


@dp.message(Command('start'))
async def send_welcome(message: Message) -> None:
    await message.answer(
        'Привет! клёво, что обратился!\n'
        'Вот план действий:\n '
        f"1. введи команду [/{CommandsEnum.add_rule.value}](/{CommandsEnum.add_rule.value})\n"
        'Пример:\n'
        f'{make_example_with_description(message)}',
        parse_mode=ParseMode.MARKDOWN
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
    rules = make_rules_from_message(message)
    rule = await MessageCRUDService(db_session).add_rule(rules)
    await message.answer(
        'Создал правило:\n'
        f'{make_chat_rule_description(rule)}\n\n'
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


def make_chat_rule_description(rule: ChatRulesDTO) -> str:
    regexps = [r.regexp for r in rule.rules]
    forward_to = rule.chat_to_forward or rule.owner_chat_id
    return (f'чат: {rule.chat_name or rule.target_chat_id}\nправила: {regexps}\n'
            f'пересылаю сообщения в чат: {forward_to}')


@dp.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message):
    # do something with error
    await message.answer("Oops, something went wrong!")


# @dp.error(ExceptionTypeFilter(AppError), F.update.message.as_("message"))
# async def handle_my_custom_exception(event: ErrorEvent, message: Message):
#     # do something with error
#     await message.answer(message)
