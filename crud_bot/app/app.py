import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from crud_bot.app.bot import bot, dp
from crud_bot.app.config import config
from crud_bot.app.db import db_client
from crud_bot.app.logger import logger
from crud_bot.views.health_check import healthcheck_route
from crud_bot.app.logging_configuration import init_logging
from crud_bot.views.views import router
from message_observer.app.start_app import observe_chats
from message_observer.app.config import config as message_observer_config


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        background_tasks = set()
        logger.info('Starting up!')
        db_client()
        if config.DEBUG is True and (ping := await db_client.admin.command('ping')):
            logger.debug(f'DB works! ping:\n{ping}')
        await bot.set_webhook(
            url=config.WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        logger.info('webhoooks set')
        task = asyncio.create_task(observe_chats())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
        yield
        logger.info('Shutting down!')
        message_observer_config.STOPPED = True
        task.cancel()
        await asyncio.wait([task])
        await bot.delete_webhook()
        db_client.close()

    if config.INIT_LOGGING:
        init_logging()

    fastapi_params = {
        'title': config.APP_NAME,
        'lifespan': lifespan,
    }

    app = FastAPI(**fastapi_params)

    app.include_router(healthcheck_route, prefix='/api/v1', tags=['v1'])
    app.include_router(router, prefix='/api/v1', tags=['v1'])

    return app
