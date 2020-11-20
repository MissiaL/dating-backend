import logging

from loguru import logger

LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'loguru': {
            'level': 'INFO',
            'class': 'app.logger.logging_config.InterceptHandler',
        }
    },
    'root': {'handlers': ['loguru'], 'propagate': True},
}


class InterceptHandler(logging.Handler):
    """Handler for catch and run logs of third-party libraries through our sinks."""

    def emit(self, record: logging.LogRecord) -> None:
        logger_opt = logger.opt(exception=record.exc_info).bind(system=True)
        logger_opt.log(record.levelname, record.getMessage())
