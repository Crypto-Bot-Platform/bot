import unittest

from common.exchangeadapter.mock import MockExchangeAdapter
from common.transaction.manager import TransactionManager


class TestTransactionManager(unittest.TestCase):
    def setUp(self) -> None:
        self.tm = TransactionManager([MockExchangeAdapter('binanceus')])

    def test_validate_transaction(self):
        is_valid = self.tm.validate('binanceus', 'BTC/USD', 'buy', 'market', 0.0001)
        self.assertTrue(is_valid)
        is_valid = self.tm.validate('binanceus', 'BTC/USD', 'buy', 'market', 0.0000009)
        self.assertFalse(is_valid)
