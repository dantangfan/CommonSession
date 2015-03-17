# -*- coding:utf-8 -*-


from CommonSession.redisSession import RedisSession
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import redis

connection = redis.Redis(host="127.0.0.1", port=6379, db=0)


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def prepare(self):
        self.session = self._create_session()

    def _create_session(self):
        """
        It's necessary to def this function, this can make sure you get a write session.
        when the session does not exist or expired, it gives you a new session.
        :return:
        """
        settings = self.application.settings
        session_id = self.get_secure_cookie(settings.get('session_cookie_name', 'session_id'))
        kwargs = dict(ip_address=self.request.remote_ip,
                      user_agent=self.request.headers.get('User-Agent'))
        old_session = RedisSession.load(session_id, connection)
        if old_session is None or old_session._is_expired():
            new_session = RedisSession(connection, **kwargs)
            self.set_secure_cookie(settings.get('session_cookie_name', 'session_id'), new_session.session_id)
        else:
            return old_session
        return new_session


class MainHandler(BaseHandler):
    def get(self):
        # we can get the session data by session.data
        print self.session.session_id
        return self.write("""
        <h2>Hello world!</p>
        """)


handler = [(r'/',MainHandler), ]
settings = {"session_cookie_name":'session_id',
            "cookie_secret":'ssssssssssssssssssssss',
            "debug":True}

app = Application(handler, **settings)
server = HTTPServer(app)
server.listen(8000)
print "server start"
IOLoop.instance().start()
