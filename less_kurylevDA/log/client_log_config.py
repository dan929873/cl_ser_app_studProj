import logging


logging.basicConfig(
    filename="logs/client.log",
    format="%(asctime)-10s %(levelname)-10s %(module)-10s %(message)-20s",
    level=logging.DEBUG,
)

LOG = logging.getLogger('app.basic')

if __name__ == '__main__':
    LOG.debug('Отладочная информация')
    LOG.info('Информационное сообщение')
    LOG.warning('Предупреждение')
    LOG.critical('Критическое общение')