import json
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM
import logging
import traceback
import inspect
from errors import ReqFieldMissingError, ServerError
import argparse
import select


# Порт по умолчанию для сетевого ваимодействия
PORT = 7777
# IP адрес по умолчанию для подключения клиента
IP = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка
ENCODING = 'utf-8'

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACC_NAME = 'account_name'
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
SENDER = 'sender'
ACCOUNT_NAME = 'account_name'


def to_byte(s, myDict):
    s.send(json.dumps(myDict).encode(encoding=ENCODING))


def from_byte(myByts):
    enc_mess = myByts.recv(MAX_PACKAGE_LENGTH)
    if isinstance(enc_mess, bytes):
        res = json.loads(enc_mess.decode(ENCODING))
        if isinstance(res, dict):
            return res
        raise ValueError
    raise ValueError
    # my_str = myByts.decode(encodings=ENCODING)
    # return json.loads(my_str)


CODE_RES = [
    {"response": 100, "alert": "basic notification"},
    {"response": 101, "alert": "important notice"},
    {"response": 200, "alert": "OK"},
    {"response": 201, "alert": "object has been created"},
    {"response": 202, "alert": "confirmation"},
    {"response": 400, "alert": "invalid request/JSON object"},
    {"response": 401, "alert": "not authorized"},
    {"response": 402, "error": "wrong login/password"},
    {"response": 403, "alert": "user is blocked"},
    {"response": 404, "alert": "user/chat is not present on the server"},
    {"response": 409, "error": "already a connection with the specified login"},
    {"response": 410, "alert": "destination exists but is not available (offline)"},
    {"response": 500, "alert": "Server error"}
]
