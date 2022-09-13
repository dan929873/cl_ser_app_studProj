# 1. Начать реализацию класса «Хранилище» для серверной стороны. Хранение необходимо осуществлять в базе данных. В качестве СУБД использовать sqlite. Для взаимодействия с БД можно применять ORM.
# Опорная схема базы данных:
# На стороне сервера БД содержит следующие таблицы:
# a) все пользователи:
# * логин;
# * информация (время последнего входа).
# b) активные пользователи:
# * id_клиента
# * время входа;
# * ip-адрес;
# * port.
# с) история клиента:
# * id_клиента
# * время входа;
# * ip-адрес;
# * port.

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


class ServerDB:
    Base = declarative_base()

    class AllUsers(Base):
        __tablename__ = 'all_users'
        # *логин;
        # *информация(время последнего входа).
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_conn = Column(DateTime)

        def __init__(self, login):
            self.login = login
            self.last_conn = datetime.datetime.now()

    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        # *id_клиента
        # *время входа;
        # *ip - адрес;
        # *port.
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        time_conn = Column(DateTime)

        def __int__(self, user, ip, port, time_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.time_conn = time_conn

    class LoginHistory(Base):
        __tablename__ = 'login_history'
        # * id_клиента
        # * время входа;
        # * ip-адрес;
        # * port.
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        last_conn = Column(DateTime)

        def __int__(self, user, ip, port, last_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.last_conn = last_conn

    def __init__(self):
        # Создаём движок базы данных
        # SERVER_DATABASE - sqlite:///server_base.db3
        # echo=False - отключает вывод на экран sql-запросов)
        # pool_recycle - по умолчанию соединение с БД через 8 часов простоя обрывается
        # Чтобы этого не случилось необходимо добавить pool_recycle=7200 (переустановка
        #    соединения через каждые 2 часа)
        self.engine = create_engine('sqlite://server_base.db3', echo=False, pool_recycle=7200)
        # создание таблиц
        self.Base.metadata.create_all(self.engine)
        # Создаём сессию
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        # когда устанавливаем соединение во время соединения
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):

        res = self.session.query(self.AllUsers).filter_by(logging=username)
        # обновляем время, если нашли
        if res.count():
            user = res.first()
            user.last_conn = datetime.datetime.now()
        else:
            user = self.AllUsers(username)
            self.session.add(user)
            # для записи ID
            self.session.commit()

        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.LoginHistory(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(history)

        self.session.commit()

