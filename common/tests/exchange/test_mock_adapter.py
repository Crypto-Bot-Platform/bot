import datetime
import unittest
from os import environ

from common.exchangeadapter.mock import MockExchangeAdapter
from common.time.time import Time


class TestMockExchangeAdapter(unittest.TestCase):
    def setUp(self) -> None:
        environ['BOT_ID'] = "unit-testing-1"
        self.adapter = MockExchangeAdapter("binanceus", Time())

    def test_fetch_balance(self):
        balance = self.adapter.fetch_balance()
        self.assertIsNotNone(balance)
        self.assertIsNotNone(balance['free'])
        self.assertIsNotNone(balance['used'])
        self.assertIsNotNone(balance['total'])

    def test_get_price(self):
        price = self.adapter.get_price('BTC/USD')
        self.assertIsNotNone(price)
        adapter = MockExchangeAdapter('binanceus', Time(datetime.datetime.now() - datetime.timedelta(hours=12)))
        price1 = adapter.get_price('BTC/USD')
        self.assertIsNotNone(price1)
        self.assertNotEqual(price, price1)

    def test_create_order(self):
        balance_start = self.adapter.fetch_balance()
        order1 = self.adapter.create_order('ETH/BTC', 'market', 'buy', 1)
        self.assertIsNotNone(order1)
        order2 = self.adapter.create_order('ETH/BTC', 'market', 'sell', 1)
        self.assertIsNotNone(order2)
        balance_end = self.adapter.fetch_balance()
        self.assertLess(balance_end['BTC']['total'], balance_start['BTC']['total'])

    def test_fetch_orders(self):
        self.test_create_order()
        orders = self.adapter.fetch_orders()
        self.assertIsNotNone(orders)
        self.assertTrue(len(orders)>2)
        print(orders)

    def test_fetch_order(self):
        order1 = self.adapter.create_order('ETH/BTC', 'market', 'buy', 0.01)
        order11 = self.adapter.fetch_order(order1['id'])
        self.assertIsNotNone(order11)
        self.assertEqual(order1['id'], order11['id'])
        order2 = self.adapter.create_order('ETH/BTC', 'market', 'sell', 0.01)
        order22 = self.adapter.fetch_order(order2['id'])
        self.assertIsNotNone(order22)
        self.assertEqual(order2['id'], order22['id'])

