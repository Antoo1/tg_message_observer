import logging.config

from pythonjsonlogger.jsonlogger import JsonFormatter

from .config import config, Environment


MEGABYTE = 1024 * 1024


is_local = (config.ENVIRONMENT.upper() == Environment.LOCAL)
default_handlers = ['console'] if is_local else ['filebeat']
filebeat_handler = {
    'filebeat': {
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'filebeat',
        'filename': '/var/log/filebeat.log',
        'backupCount': 1,
        'maxBytes': 3 * MEGABYTE,
        'filters': [],
    },
}


LOGGING_CONFIG = {
    'version': 1,
    'filters': {
    },
    'formatters': {
        'default': {
            'format': (
                '%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:\n%(message)s\n'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'filebeat': {
            'format': (
                '%(levelname)s::%(asctime)s:%(name)s.%(funcName)s:'
                '%(message)s'
            ),
            '()': JsonFormatter,
            'json_ensure_ascii': False,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            'filters': [],
        },
        **({} if is_local else filebeat_handler)
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': default_handlers,
        },
        config.APP_NAME: {
            'level': config.LOG_LEVEL,
            'handlers': default_handlers,
            'propagate': False
        },
    },
    'disable_existing_loggers': False,
}


def init_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
