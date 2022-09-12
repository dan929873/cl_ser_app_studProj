# -*- coding: utf-8 -*-
import inspect
import sys
import traceback

from base import *
import log.client_log_config
import log.server_log_config

if sys.argv[0].find('client') == -1:
    LOG = logging.getLogger('server')
else:
    LOG = logging.getLogger('client')

def log (fun):

    def log_save(*args,**kwargs):
        res = fun(*args,**kwargs)
        LOG.debug(f'Была вызвана функция {fun.__name__} c параметрами {args}, {kwargs}.'
                  f'Вызов из модуля {fun.__module__}.'
                  f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                  , stacklevel=2)
        return res
    return log_save