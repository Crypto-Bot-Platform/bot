import unittest
from datetime import timedelta
from os import environ
from common.exchangeadapter.mock import MockExchangeAdapter
from common.openorder.manager import OpenOrderManager


class TestOpenOrdersManager(unittest.TestCase):
    def setUp(self) -> None:
        self.exchange = MockExchangeAdapter('binanceus')
        self.oom = OpenOrderManager([self.exchange], timedelta(seconds=30))

    def test_monitor_open_orders(self):
        order = self.exchange.create_order('ETH/BTC', 'market', 'buy', 0.01)
        self.oom.start('binanceus', 'ETH/BTC', order['id'])
