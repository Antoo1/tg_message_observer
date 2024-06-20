import os
from typing import Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

ENVIRONMENT = os.environ['ENVIRONMENT'].upper()
CONFIG_FILE = os.environ.get('CONFIG_FILE', f'./config/{ENVIRONMENT.lower()}.yml')


class ABSBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(yaml_file=CONFIG_FILE, extra='ignore')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return env_settings, YamlConfigSettingsSource(settings_cls)


class BaseConfig(ABSBaseConfig):
    ENVIRONMENT: str

    @property
    def ENVIRONMENT(self) -> str:
        return ENVIRONMENT

    INIT_LOGGING: bool = True
    DEBUG: bool = False
    LOG_LEVEL: str = 'INFO'
    APP_NAME: str

    TG_API_TOKEN: str
    WEBHOOK_URL: str

    DB_NAME: str
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_SCHEMA: str
    DB_POOL_SIZE: int = 5

    @property
    def ASYNC_DB_URL(self) -> str:
        return f'postgresql+asyncpg://{self._get_db_url_wo_driver()}'

    def _get_db_url_wo_driver(self):
        return '{user}:{password}@{host}:{port}/{database}'.format(
            user=self.DB_LOGIN,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )


class Environment:
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    TEST = 'TEST'
    DEV = 'DEV'
    PROD = 'PROD'


class DevConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    """Для запуска юнит тестов"""
    INIT_LOGGING: bool = False
    TESTING: bool = True
    DEBUG: bool = True


class ProdConfig(BaseConfig):
    pass


class LocalConfig(BaseConfig):
    pass


config_class: Type[BaseConfig] = {
    Environment.LOCAL: LocalConfig,
    Environment.TESTING: TestingConfig,
    Environment.DEV: DevConfig,
    Environment.TEST: TestConfig,
    Environment.PROD: ProdConfig,
}.get(ENVIRONMENT, BaseConfig)

config: BaseConfig = config_class()
