import unittest

from redirect import redir


class TestRedir(unittest.TestCase):

    def setUp(self):
        self.datastore = redir.DataStore()

    def test_getter_setter(self):
        assert self.datastore.get('key') is None
        self.datastore['key'] = 'value'
        assert self.datastore.get('key') == 'value'
        assert self.datastore['key'] == 'value'

    def test_redirect_one_level(self):
        self.datastore['1'] = '2'
        assert self.datastore.redirect('1') == '2'

    def test_redirect_three_levels(self):
        self.datastore['1'] = '2'
        self.datastore['2'] = '3'
        self.datastore['3'] = '4'
        assert self.datastore.redirect('1') == '4'
        assert self.datastore.redirect('2') == '4'
        assert self.datastore.redirect('3') == '4'

    def test_redirect_cycle_detection(self):
        self.datastore['1'] = '2'
        self.datastore['2'] = '1'
        with self.assertRaises(redir.RedirectException):
            self.datastore.redirect('1')

    def test_todict(self):
        assert self.datastore.todict() == {}
        data = { '1': '2', '2': '3' }
        for k, v in data.iteritems():
            self.datastore[k] = v
        assert self.datastore.todict() == data

    def test_contains(self):
        self.datastore['key'] ='value'
        assert 'key' in self.datastore



class TestRedisRedir(TestRedir):

    def setUp(self):
        self.datastore = redir.RedisDataStore(number=15)
        pass

    def tearDown(self):
        # TODO: fix crash when REDIS_PORT_6379_TCP_PORT env variable doesn't exist
        # self.datastore.clear_all()
        pass
