#!/usr/local/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Rocky Peng'

from datetime import datetime
import time
import random
import string
from hashlib import md5

from web.utils.log import Logger
from web.models.users import Users
from web.services.hosts import hosts
from web.services.projects import projects
from .base import Base
from web.utils.error import Error
from .sessions import sessions


logger = Logger("user service")


class UsersService(Base):
    __model__ = Users

    def login(self, username, password):
        # password = md5(password).hexdigest().upper()
        password_md5 = md5(password.encode()).hexdigest().upper()   # for python3
        user = self.first(name=username, password=password_md5)
        logger.info('%s, %s -> %s -> %s' % (username, password, password_md5, user))
        if user is None:
            raise Error(13000)
        session = sessions.first(user_id=user.id)
        expired = datetime.fromtimestamp(time.time()+24*60*60).isoformat()
        if session is None:
            # sign = ''.join(random.choice(string.letters+string.digits) for _ in range(20))
            sign = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(20))    # for python3
            sessions.create(user_id=user.id,
                session=sign,
                expired=expired)
        else:
            sessions.update(session, expired=expired)
            sign = session.session
        return sign

    def logout(self, user):
        session = sessions.first(user_id=user.id)
        if session is not None:
            sessions.update(
                session,
                expired=datetime.now().isoformat())


    def is_login(self, session, apikey):
        if users.first(apikey=apikey):
            return True
        session = sessions.first(session=session)
        if session is not None:
            if (session.expired-datetime.now()).total_seconds() > 0:
                return True
        return False

    def get_user_hosts(self, user, **kargs):
        if user.role == user.ROLE["ADMIN"]:
            return dict(hosts=hosts.all(kargs.get("offset"), kargs.get("limit"), kargs.get("order_by")),
                        count=hosts.count())
        else:
            return dict(hosts=user.hosts.all(),
                        count=user.hosts.count())

    def get_user_projects(self, user, **kargs):
        if user.role == user.ROLE["ADMIN"]:
            return dict(projects=projects.all(kargs.get("offset"), kargs.get("limit"), kargs.get("order_by")),
                        count=projects.count())
        else:
            return dict(projects=user.projects.all(),
                        count=user.projects.count())


users = UsersService()
