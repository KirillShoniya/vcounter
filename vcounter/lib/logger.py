import logging
import sys

from loguru import logger

from vcounter.lib.config import Config


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


config = Config()
level = logging.INFO if not config.debug else logging.DEBUG
rotation_after, retention = config.log_rotation_settings

# remove default logging handler
logger.remove(0)

logger.add(
    sys.stdout,
    level=logging.getLevelName(level),
    format='[{time}] -- {level} -- {message}')

logger.add(
    config.log_file_path,
    rotation=rotation_after,
    retention=retention,
    level=logging.getLevelName(level),
    format='[{time}] -- {level} -- {message}')

# replace default logging with loguru
logging.basicConfig(handlers=[InterceptHandler()], level=level)
