from functools import partial

from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative

from group_observer.common.db import BaseModel
from group_observer.app.config import config
from group_observer.common.db import setup_db_engine
from group_observer.common.lazy_init_wrapper import LazyInitWrapper

db_engine = LazyInitWrapper(partial(setup_db_engine, config))
BaseModel = as_declarative(metadata=MetaData(schema=config.DB_SCHEMA))(BaseModel)
