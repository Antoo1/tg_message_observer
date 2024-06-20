from sqlalchemy import Column, BigInteger, inspect
from sqlalchemy.orm import sessionmaker, ColumnProperty
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from group_observer.app.config import BaseConfig


class BaseModel:
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # noqa: A003

    def to_dict(self):
        model = self
        fields_prop = {
            key: getattr(model, key)
            for key, value in inspect(model).mapper.all_orm_descriptors.items()
            if not hasattr(value, 'original_property') and hasattr(value, 'prop') and isinstance(
                value.prop, (ColumnProperty,))
        }

        return fields_prop


def setup_db_session(db_engine):
    return sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        autoflush=True,
        autocommit=False,
        expire_on_commit=False,
    )


def setup_db_engine(config: BaseConfig) -> AsyncEngine:
    return create_async_engine(
        config.ASYNC_DB_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=config.DB_POOL_SIZE,
        connect_args={
            'command_timeout': 60,
            'server_settings': {
                'application_name': config.APP_NAME
            }
        },
        echo=config.DEBUG,
    )
