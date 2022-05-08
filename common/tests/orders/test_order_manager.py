import unittest
from datetime import timedelta
from os import environ

from common.exchangeadapter.mock import MockExchangeAdapter
from common.openorder.manager import OpenOrderManager
from common.order.manager import OrderManager


class TestOrdersManager(unittest.TestCase):
    def setUp(self) -> None:
        environ['BOT_ID'] = "unit-testing-1"
        exchange = MockExchangeAdapter('binanceus')
        oom = OpenOrderManager([exchange], timedelta(seconds=30))
        self.om = OrderManager([exchange], oom)

    def test_execute_order(self):
        self.om.execute('binanceus', 'ETH/BTC', 'buy', 'market', 0.01)
