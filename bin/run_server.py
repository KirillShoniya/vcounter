from vcounter.server import app
from vcounter.server import config
from vcounter.lib.logger import logger


if __name__ == '__main__':
    logger.info('Server started')
    app.run(host=config.server_host, port=config.server_port, debug=config.debug)
