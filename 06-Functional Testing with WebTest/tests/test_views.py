import unittest
from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_view(self):
        from myapp.views import home_view
        request = testing.DummyRequest()
        response = home_view(request)
        self.assertIn(b'Testing Tutorial', response.body)

    def test_api_view(self):
        from myapp.views import api_view
        request = testing.DummyRequest()
        info = api_view(request)
        self.assertEqual(info['status'], 'ok')
        self.assertEqual(len(info['data']), 5)