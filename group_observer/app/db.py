from functools import partial

from group_observer.app.config import config
from group_observer.common.db import setup_db_engine
from group_observer.common.lazy_init_wrapper import LazyInitWrapper

db_client = LazyInitWrapper(partial(setup_db_engine, config))
