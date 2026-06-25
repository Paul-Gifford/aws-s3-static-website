import json
import unittest
from unittest.mock import MagicMock, patch

# Mock boto3 before importing the lambda function
import sys
sys.modules['boto3'] = MagicMock()

import importlib
import lambda_function

class TestVisitorCounter(unittest.TestCase):

    @patch('lambda_function.table')
    def test_returns_200(self, mock_table):
        """Lambda should return a 200 status code"""
        mock_table.update_item.return_value = {
            'Attributes': {'count': 5}
        }
        result = lambda_function.lambda_handler({}, {})
        self.assertEqual(result['statusCode'], 200)

    @patch('lambda_function.table')
    def test_returns_count(self, mock_table):
        """Lambda should return a count in the body"""
        mock_table.update_item.return_value = {
            'Attributes': {'count': 5}
        }
        result = lambda_function.lambda_handler({}, {})
        body = json.loads(result['body'])
        self.assertIn('count', body)
        self.assertEqual(body['count'], 5)

    @patch('lambda_function.table')
    def test_cors_headers(self, mock_table):
        """Lambda should return CORS headers"""
        mock_table.update_item.return_value = {
            'Attributes': {'count': 5}
        }
        result = lambda_function.lambda_handler({}, {})
        self.assertEqual(result['headers']['Access-Control-Allow-Origin'], '*')

if __name__ == '__main__':
    unittest.main()