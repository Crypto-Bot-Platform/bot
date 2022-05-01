import unittest
from os import environ
from common.exchangeadapter.default import DefaultExchangeAdapter


class TestDefaultExchangeAdapter(unittest.TestCase):
    def setUp(self) -> None:
        test_exchange = environ["TEST_EXCHANGE_NAME"] if "TEST_EXCHANGE_NAME" in environ else "binanceus"
        api_key = environ['TEST_EXCHANGE_API_KEY'] if 'TEST_EXCHANGE_API_KEY' in environ else None
        secret = environ['TEST_EXCHANGE_SECRET'] if 'TEST_EXCHANGE_SECRET' in environ else None
        password = environ['TEST_EXCHANGE_PASSWORD'] if 'TEST_EXCHANGE_PASSWORD' in environ else None
        self.adapter = DefaultExchangeAdapter(test_exchange, {
            'apiKey': api_key,
            'secret': secret,
            'password': password
        })

    def test_fetch_balance(self):
        result = self.adapter.fetch_balance()
        print(result)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result['timestamp'])
        self.assertIsNotNone(result['datetime'])
        self.assertIsNotNone(result['free'])
        self.assertIsNotNone(result['used'])
        self.assertIsNotNone(result['total'])

    def test_get_price(self):
        result = self.adapter.get_price('BTC/USD')
        print(result)
        self.assertTrue(result > 0)

    def test_get_fees(self):
        mf = self.adapter.get_maker_fee('BTC/USD')
        tf = self.adapter.get_taker_fee('BTC/USD')
        self.assertIsNotNone(mf)
        self.assertIsNotNone(tf)


if __name__ == '__main__':
    unittest.main()
