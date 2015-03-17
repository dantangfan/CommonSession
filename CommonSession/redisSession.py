# -*- coding:utf-8 -*-

from baseSession import BaseSession
try:
    import redis
except Exception, e:
    print 'Please install redis and python-redis before run this program'
    exit(0)


class RedisSession(BaseSession):
    """
    Redis session, use session_id as key and save in redis-set.
    """

    def __init__(self, connection, **kwargs):
        super(RedisSession, self).__init__(**kwargs)
        self.connection = connection
        if not kwargs.has_key('session_id'):
            self.save()

    def save(self):
        value = self.serialize()
        self.connection.set(self.session_id, value)
        try:
            self.connection.bgsave()
        except redis.ResponseError:
            pass

    @staticmethod
    def load(session_id, connection):
        if connection.exists(session_id) == 1:
            try:
                data = connection.get(session_id)
                kwargs = RedisSession.deserialize(data)
                return RedisSession(connection, **kwargs)
            except:
                return None
        return None

    def delete(self):
        self.connection.delete(self.session_id)
        try:
            self.connection.bgsave()
        except:
            pass