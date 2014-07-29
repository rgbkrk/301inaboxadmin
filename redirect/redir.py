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

    def __init__(self):
        #TODO(tvoran): get host and port from config or env
        redis_host = os.environ.get('REDIS_PORT_6379_TCP_ADDR')
        redis_port = os.environ.get('REDIS_PORT_6379_TCP_PORT')
        self.redis_conn = StrictRedis(host=redis_host, port=redis_port, db=0)

    def __setitem__(self, k, v):
        self.redis_conn.set(k, v)

    def __getitem__(self, k):
        return self.redis_conn.get(k)

    def get(self, k):
        return self.redis_conn.get(k)

    def todict(self):
        #TODO(tvoran): use paginate
        #TODO(tvoran): scan doesn't seem to work...
        data = {}
        for key, value in self.redis_conn.scan():
            data[key] = value
        return data
