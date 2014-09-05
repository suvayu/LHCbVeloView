import unittest2 as unittest

import velo_monitor


class TestPages(unittest.TestCase):
    def setUp(self):
        self.app = velo_monitor.create_app()
        self.client = self.app.test_client()

    def test_index_page(self):
        """The index page should show the app's info and the correct route."""
        rv = self.client.get('/')
        assert self.app.config['APP_NAME'] in rv.data
        assert self.app.config['APP_DESCRIPTION'] in rv.data


if __name__ == '__main__':
    unittest.main()
