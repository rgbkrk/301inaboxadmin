from redis import StrictRedis
import os

class RedirectException(Exception):
    def __init__(self, msg):
        super(Exception, self).__init__(msg)

class DataStore(object):
    """Our abstracted datastore. This base class is just a dictionary.
    Subclass this and override the __setitem__, __getitem__, and get
    methods to use some other storage."""

    def __init__(self):
        self.data = {}

    def __setitem__(self, k, v):
        self.data[k] = v

    def __getitem__(self, k):
        return self.data[k]

    def __delitem__(self, k):
        del self.data[k]

    def get(self, k):
        return self.data.get(k)

    def __contains__(self, k):
        return k in self.data

    def redirect(self, url):
        """Really basic redirect algorithm with cycle detection."""
        # todo: use Flask's redirect support
        seen_urls = set([url])
        from_url = url
        while True:
            to_url = self.get(from_url)
            if to_url is None:
                break
            if to_url in seen_urls:
                raise RedirectException('Saw redirect loop with key {0}'.format(url))
            from_url = to_url
        return from_url

    def todict(self):
        data = {}
        for key, value in self.data.iteritems():
            data[key] = value
        return data


class RedisDataStore(DataStore):
    """Redis-backed datastore object."""

    def __init__(self, number=0):
        redis_host = os.environ.get('REDIS_PORT_6379_TCP_ADDR')
        redis_port = os.environ.get('REDIS_PORT_6379_TCP_PORT')
        self.redis_conn = StrictRedis(host=redis_host, port=redis_port,
                                      db=number)

    def __setitem__(self, k, v):
        self.redis_conn.set(k, v)

    def __getitem__(self, k):
        return self.redis_conn.get(k)

    def __delitem__(self, k):
        self.redis_conn.delete(k)

    def get(self, k):
        return self.redis_conn.get(k)

    def __contains__(self, k):
        return self.redis_conn.exists(k)

    def todict(self):
        #TODO(tvoran): use paginate
        #TODO(tvoran): do something besides multiple gets
        data = {}
        for key in self.redis_conn.keys():
            data[key] = self.get(key)
        return data

    def clear_all(self):
        self.redis_conn.flushdb()
