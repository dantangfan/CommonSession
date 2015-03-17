# -*- coding:utf-8 -*-

import datetime
import os
import collections
import base64
import pickle


class BaseSession(collections.MutableMapping):
    """
    This is the base class for a session class.
    You can either use MySQL, Redis, Mongo or even file to save your session.
    It is easy to extend the class to make a session. Subclass can just rewrite
    load(). save() and delete() to reach the target.
    """
    def __init__(self,
                 session_id=None,
                 data=None,
                 expire_time=None,
                 expire_at=None,
                 ip_address=None,
                 user_agent=None,
                 **kwargs
                 ):
        if session_id:
            self.session_id = session_id
            self.data = data
            self.expire_time = expire_time
            self.expire_at = expire_at
        else:
            self.session_id = self._new_session_id()
            self.data = dict()
            self.expire_time = expire_time
            self.expire_at = self._expire_at()
        self.ip_address = ip_address
        self.user_agent = user_agent

    def __repr__(self):
        return "<session id: %s WITH data: %s>" % (self.session_id, self.data)

    def __str__(self):
        return self.session_id

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return self.data.__iter__()

    def keys(self):
        return self.data.keys()

    def _new_session_id(self, session_string=None):
        if session_string:
            return session_string
        return os.urandom(32).encode("hex")

    def _expire_at(self):
        """
        Get expiration time, default 1 hour
        :return: datetime.datetime
        """
        if self.expire_time is None:
            return None
        elif isinstance(self.expire_time, (int, long, str)):
            self.expire_time = datetime.timedelta(seconds=int(self.expire_time))
        elif isinstance(self.expire_time, datetime.timedelta):
            pass
        else:
            self.expire_time = datetime.timedelta(seconds=3600)
        return datetime.datetime.utcnow() + self.expire_time

    def _is_expired(self):
        """
        Check if the session is expired
        :return: boolean
        """
        if self.expire_at is None:
            return False
        return datetime.datetime.utcnow() >= self.expire_at

    def refresh(self, expire_time, new_session=False):
        """
        Refresh a session for longer exist of a user, you may need to create a new session_id for some reason
        :param expire_time:
        :param new_session:
        :return:
        """
        if expire_time:
            self.expire_time = expire_time
        else:
            pass
        self.expire_at = self._expire_at()
        if new_session:
            self.delete()
            self.session_id = self._new_session_id()
        self.save()

    def save(self):
        """
        Save session msg in db
        :return:
        """
        pass

    @staticmethod
    def load(session_id, connection):
        """
        Load the session you want
        Return None if not found
        :return:
        """
        pass

    def delete(self):
        """
        Delete all data of the session from db
        :return:
        """
        pass

    def serialize(self):
        value = dict(
            session_id=self.session_id,
            data=self.data,
            expire_time=self.expire_time,
            expire_at=self.expire_at,
            ip_address=self.ip_address,
            user_agent=self.user_agent
        )
        return base64.encodestring(pickle.dumps(value))

    @staticmethod
    def deserialize(string):
        return pickle.loads(base64.decodestring(string))