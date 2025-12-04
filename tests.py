import sys
import os
import unittest
from unittest.mock import MagicMock
import importlib

# Mock db module before importing app
sys.modules['db'] = MagicMock()

import app

class TestWinedentity(unittest.TestCase):
    def setUp(self):
        pass

    def test_local_mode(self):
        """Test LOCAL mode routing"""
        # Set ENV to LOCAL and reload app
        os.environ['ENV'] = 'LOCAL'
        importlib.reload(app)
        client = app.app.test_client()
        
        # Test Homepage
        resp = client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Mer informasjon kommer snart!', resp.data)

        # Test Registration
        resp = client.get('/reg')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Medlemskapsregistrering', resp.data)

    def test_prod_mode(self):
        """Test PROD mode routing"""
        # Unset ENV and reload app
        if 'ENV' in os.environ:
            del os.environ['ENV']
        importlib.reload(app)
        client = app.app.test_client()

        # Test Homepage (winedentity.org)
        resp = client.get('/', headers={'Host': 'winedentity.org'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Mer informasjon kommer snart!', resp.data)

        # Test Registration (reg.winedentity.org)
        resp = client.get('/', headers={'Host': 'reg.winedentity.org'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Medlemskapsregistrering', resp.data)

        # Test 404
        resp = client.get('/', headers={'Host': 'unknown.com'})
        self.assertEqual(resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
