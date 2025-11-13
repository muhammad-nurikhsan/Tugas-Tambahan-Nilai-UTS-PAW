import unittest
from pyramid import testing
from webtest import TestApp # pyright: ignore[reportMissingImports]

class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from myapp import main
        app = main({})
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Testing Tutorial', res.body)

    def test_api_json(self):
        res = self.testapp.get('/api/data', status=200)
        self.assertEqual(res.content_type, 'application/json')
        data = res.json
        self.assertEqual(data['status'], 'ok')
        self.assertIn('data', data)

    def test_404(self):
        self.testapp.get('/notfound', status=404)