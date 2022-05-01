import unittest

from common.exchangeadapter.mock import MockExchangeAdapter
from common.portfolio.manager import PortfolioManager


class TestPortfolioManager(unittest.TestCase):
    def setUp(self) -> None:
        self.pm = PortfolioManager([MockExchangeAdapter('binanceus')])

    def test_sync(self):
        self.pm.sync('binanceus')
        self.assertIsNotNone(self.pm.balance['binanceus'])

    def test_validate(self):
        valid = self.pm.validate('binanceus', 'BTC/USD', 'buy', 'market', 1)
        self.assertFalse(valid)
