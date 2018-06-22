import os
import logging

logger = logging.getLogger(__name__)


class HealthCheckConfig(object):

    HOST_IP = None
    HEALTHCHECK_PORT = None
    HEALTHCHECK_INTERVAL = None
    SERVER_PORT = None

    @classmethod
    def get_config(cls):

        config = cls()
        config.HOST_IP = os.environ.get('HOST_IP', None)
        config.HEALTHCHECK_PORT = os.environ.get('HEALTHCHECK_PORT', None)
        config.HEALTHCHECK_INTERVAL =\
            os.environ.get('HEALTHCHECK_INTERVAL', None)
        config.SERVER_PORT = os.environ.get('SERVER_PORT', None)

        if not config.HEALTHCHECK_PORT:
            logger.error('Please specify the healthcheck port')
            return None

        if not config.HEALTHCHECK_INTERVAL:
            logger.error('Please specify the healthcheck interval')
            return None

        if not config.SERVER_PORT:
            logger.error('Please specify the server port')
            return None

        return config
