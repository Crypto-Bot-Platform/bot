import datetime
import unittest
from os import environ

from common.exchangeadapter.mock import MockExchangeAdapter
from common.openorder.manager import OpenOrderManager
from common.order.executor import OrderExecutor
from common.order.manager import OrderManager
from common.portfolio.manager import PortfolioManager
from common.schema.executor import ExecutorSchema
from common.transaction.manager import TransactionManager


class TestOrderExecutor(unittest.TestCase):
    def setUp(self) -> None:
        environ['BOT_ID'] = "unit-testing-1"
        exchange = MockExchangeAdapter('binanceus')
        self.oe = OrderExecutor([PortfolioManager([exchange]), TransactionManager([exchange])],
                                OrderManager([exchange], OpenOrderManager([exchange], datetime.timedelta(seconds=30))))
        self.oe.listen()
        self.em = self.oe.em

    def test_send_order_for_execution(self):
        self.em.send_command_to_address(f"{self.oe.bot_id}-executor", ExecutorSchema, {
            "timestamp": int(datetime.datetime.now().timestamp() * 1000),
            "exchange": 'binanceus',
            "symbol": "BTC/USD",
            "side": "buy",
            "type": "market",
            "amount": 1
        })
        self.em.send_command_to_address(f"{self.oe.bot_id}-executor", ExecutorSchema, {
            "timestamp": int(datetime.datetime.now().timestamp() * 1000),
            "exchange": 'binanceus',
            "symbol": "ETH/BTC",
            "side": "sell",
            "type": "market",
            "amount": 0.001
        })
