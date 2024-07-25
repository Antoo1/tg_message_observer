from functools import partial

from crud_bot.app.config import config
from crud_bot.common.db import setup_db_engine
from crud_bot.common.lazy_init_wrapper import LazyInitWrapper

db_client = LazyInitWrapper(partial(setup_db_engine, config))
