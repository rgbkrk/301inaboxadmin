import unittest

from redirect import app


def store_record(hostname, url):
    app.recordstore[hostname] = url


class TestApp(unittest.TestCase):
    def setUp(self):
        app.start()

    def test_check_cycle(self):
        store_record("x.com", "y.com")
        store_record("y.com", "z.com")
        self.assertTrue(app._creates_cycle("z.com", "x.com"), "Cycle not detected")