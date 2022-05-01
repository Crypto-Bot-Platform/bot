import math

from pymongo import MongoClient


class ExchangeAdapter:
    def __init__(self, exchange_name: str):
        self.exchangeName = exchange_name
        self.client = MongoClient()
        self.meta = self.client['cbp']['exchanges'].find_one({"_id": exchange_name})

    def create_order(self, symbol: str, type: str, side: str, amount, price=None, params={}):
        raise NotImplemented()

    def cancel_order(self, id: str, symbol: str = None, params={}):
        raise NotImplemented()

    def fetch_orders(self, symbol: str = None, since: int = None, limit: int = None, params={}):
        raise NotImplemented()

    def fetch_order(self, id: str, symbol: str = None, params={}):
        raise NotImplemented()

    def get_price(self, symbol: str, params={}) -> float:
        raise NotImplemented()

    def get_maker_fee(self, symbol: str, params={}) -> float:
        return self.meta['markets'][symbol]['maker']

    def get_taker_fee(self, symbol: str, params={}) -> float:
        return self.meta['markets'][symbol]['taker']

    def get_amount_limit(self, symbol: str, params={}) -> (float, float):
        limits = self.meta['markets'][symbol]['limits']['amount']
        return limits['min'] if limits['min'] else -math.inf, limits['max'] if limits['max'] else math.inf

    def fetch_balance(self, params={}):
        raise NotImplemented()
