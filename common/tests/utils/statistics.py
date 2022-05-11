import datetime
import unittest
from datetime import time

from common.exchangeadapter.mock import MockExchangeAdapter
from common.portfolio.manager import PortfolioManager
from common.utils.statistics import StatisticsRecorder


class TestStatisticsRecorder(unittest.TestCase):
    def setUp(self) -> None:
        self.pm = PortfolioManager([MockExchangeAdapter('binanceus')])
        self.sr = StatisticsRecorder()

    def test_send_portfolio(self):
        self.sr.async_post_portfolio(self.pm.balance)

    def test_send_health_log(self):
        self.sr.post_health_check()

    def test_send_order(self):
        self.sr.post_order({
            'id': '1234567890',
            'clientId': 'bot_id_123',
            'datetime': datetime.datetime.now(),
            'timestamp': datetime.datetime.now().timestamp() * 1e3,
            'status': 'closed',  # Close transaction immediately
            'symbol': 'ETH/BTC',
            'type': "market",
            'timeInForce': 'GTC',
            'side': "buy",
            'price': 0.07,
            'average': 0.07,
            'amount': 1.2,
            'filled': 1.2,
            'remaining': 0,
            'cost': 0.84,
            'fee': {
                'currency': 'BTC',
                'cost': 0.001,
                'rate': 0
            }
        })
