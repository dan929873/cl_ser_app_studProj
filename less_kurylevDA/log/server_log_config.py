# https://gist.github.com/adejones/71c36c8a32990f9d6adf27758aec146b

import logging.handlers

log_file_name = 'log/logs/server.log'
logging_level = logging.DEBUG


# set TimedRotatingFileHandler for root
formatter = logging.Formatter("%(asctime)-10s %(levelname)-10s %(module)-10s %(message)-20s")
# use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="D", interval=1)
handler.setFormatter(formatter)
LOG = logging.getLogger() # or pass string to give it a name
LOG.addHandler(handler)
LOG.setLevel(logging_level)


if __name__ == '__main__':
    LOG.debug('Отладочная информация')
    LOG.info('Информационное сообщение')
    LOG.warning('Предупреждение')
    LOG.critical('Критическое общение')