import os
from typing import Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

ENVIRONMENT = os.environ['ENVIRONMENT'].upper()
CONFIG_FILE = os.environ.get('CONFIG_FILE', f'../../config/{ENVIRONMENT.lower()}.yml')


class BaseConfig(BaseSettings):
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


class Config(BaseConfig):
    ENVIRONMENT: str

    @property
    def ENVIRONMENT(self) -> str:
        return ENVIRONMENT

    INIT_LOGGING: bool = True
    ENABLE_SWAGGER: bool = False
    DEBUG: bool = False
    LOG_LEVEL: str = 'INFO'

    API_ID: int
    API_HASH: str
    APP_TITLE: str
    SHORT_NAME: str
    TEST_CONFIGURATION: str
    PROD_CONFIGURATION: str


class Environment:
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    TEST = 'TEST'
    DEV = 'DEV'
    PROD = 'PROD'


class DevConfig(Config):
    pass


class TestConfig(Config):
    pass


class TestingConfig(Config):
    """Для запуска юнит тестов"""
    INIT_LOGGING: bool = False
    TESTING: bool = True
    DEBUG: bool = True


class ProdConfig(Config):
    pass


class LocalConfig(Config):
    pass


config_class: Type[Config] = {
    Environment.LOCAL: LocalConfig,
    Environment.TESTING: TestingConfig,
    Environment.DEV: DevConfig,
    Environment.TEST: TestConfig,
    Environment.PROD: ProdConfig,
}.get(ENVIRONMENT, Config)

config: Config = config_class()
