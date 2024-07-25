import asyncio

from telethon import TelegramClient

from crud_bot.dto import ChatRulesDTO
from crud_bot.fasade import DBFasade
from message_observer.app.client import client
from message_observer.app.config import config
from message_observer.app.logger import logger
from message_observer.app.logging_configuration import init_logging

from message_observer.services import HandlerRegistryService


async def send_start_message(tg_client: TelegramClient):
    entity = await tg_client.get_entity(config.MY_USERNAME)
    await tg_client.send_message(entity, 'privet')
    logger.debug('privet sent')


async def observe_chats():
    init_logging()
    tasks = set()
    async with client:
        logger.info('starting TG client')
        await client.start()
        handler_registry = HandlerRegistryService(client)
        await send_start_message(client)
        task = asyncio.create_task(_looped_task(handler_registry))
        tasks.add(task)
        task.add_done_callback(tasks.discard)
        await client.run_until_disconnected()


async def _looped_task(handler_registry: HandlerRegistryService):
    facade = DBFasade(logger=logger)
    logger.debug('run task')

    while not config.STOPPED:
        try:
            chats: list[ChatRulesDTO] = await facade.get_rules_by_tg_id(config.MY_ID)
            handler_registry.update_handlers_if_differ(chats)
        except Exception as e:
            logger.error(f'error occurred:{e!r}')
        await asyncio.sleep(5)


if __name__ == '__main__':
    from crud_bot.app.db import db_client
    db_client()
    asyncio.run(observe_chats())
