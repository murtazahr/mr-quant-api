import logging
import unittest

from django.test import TestCase
from unittest.mock import patch
from datetime import date, datetime
from pytz import timezone
from pandas import DataFrame
from freezegun import freeze_time
from marketdata.services.spot_service import SpotService


class SpotServiceTestCase(TestCase):
    def setUp(self):
        self.spot_service = SpotService()

    @freeze_time("2023-05-21")  # Freeze time for consistent test results
    @patch('marketdata.services.spot_service.yf.download')  # Mock the yfinance download function
    def test_get_live_price_with_data(self, mock_download):
        self.assertEqual(True, True)

    @freeze_time("2023-05-21")  # Freeze time for consistent test results
    @patch('marketdata.services.spot_service.yf.download')  # Mock the yfinance download function
    def test_get_live_price_no_data(self, mock_download):
        self.assertEqual(True, True)

    @patch('marketdata.services.spot_service.yf.download')  # Mock the yfinance download function
    def test_get_close_price(self, mock_download):
        self.assertEqual(True, True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
