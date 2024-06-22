from contextlib import asynccontextmanager

from fastapi import FastAPI

from group_observer.app.bot import bot, dp
from group_observer.app.config import config
from group_observer.app.db import db_client
from group_observer.app.logger import logger
from group_observer.views.health_check import healthcheck_route
from group_observer.app.logging_configuration import init_logging
from group_observer.views.views import router


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        logger.info('Starting up!')
        db_client()
        logger.debug(await db_client.admin.command('ping'))
        await bot.set_webhook(
            url=config.WEBHOOK_URL,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        logger.info('webhoooks set')
        yield
        await bot.delete_webhook()
        db_client.close()
        logger.info("Shutting down!")

    if config.INIT_LOGGING:
        init_logging()

    fastapi_params = {
        'title': config.APP_NAME,
        'lifespan': lifespan,
    }

    app = FastAPI(**fastapi_params)

    app.include_router(healthcheck_route, prefix='/api/v1', tags=['v1'])
    app.include_router(router, prefix='/api/v1', tags=['v1'],)

    return app
