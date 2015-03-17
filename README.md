####common session

Tornado doesn't have a session module. Although its security cookie is wonderful, sometimes I still need session.

So I implement one for my daily use, and it's simple to inherit. You can chose any database you like or even use a file to record your session.

You just need to implement load(), save(), delete(), or you may add some extra data to save in the session.

###useage

```
sudo python setup.py install
```

```
from CommonSession.redisSession import RedisSession
```

Any other method, please reach the code.