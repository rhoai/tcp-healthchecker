import gevent.monkey
gevent.monkey.patch_all()

import gevent
import socket
import logging

from gevent.server import StreamServer

from config import HealthCheckConfig

logger = logging.getLogger(__name__)


HEALTHY = False
def healthcheck(address):
    global HEALTHY

    try:
        logger.debug('Checking server status')
        client = socket.create_connection(address, 3)
    except IOError:
        logger.debug('Server failed to connect')
        HEALTHY = False
    else:
        HEALTHY = True
    finally:
        logger.debug('Closing socket connection')
        client.shutdown(socket.SHUT_RD)
        client.close()


def run_healthcheck(host, port, interval):

    while True:
        healthcheck((host, port))
        logger.info('Server is healthly: {0}'.format(HEALTHY))
        gevent.sleep(interval)


def healthcheck_response(socket, address):
    global HEALTHY

    if HEALTHY:
        socket.sendall('ok')


def main():
    config = HealthCheckConfig.get_config()

    server = StreamServer(('0.0.0.0', int(config.SERVER_PORT)),
                          healthcheck_response)
    server.start()
    logger.info('server started')

    g1 = gevent.spawn(run_healthcheck, config.HOST_IP,
                      int(config.HEALTHCHECK_PORT),
                      int(config.HEALTHCHECK_INTERVAL))
    logger.info('started checking thread')
    g1.join()


if __name__ == '__main__':

    main()
