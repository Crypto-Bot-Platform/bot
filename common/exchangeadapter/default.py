from eslogger import Logger

from common.exchangeadapter.abstract import ExchangeAdapter
import ccxt


class DefaultExchangeAdapter(ExchangeAdapter):
    def __init__(self, exchange_name: str, config=None):
        super().__init__(exchange_name)
        self.name = exchange_name
        exchange_class = getattr(ccxt, exchange_name)
        if config is not None:
            self.client = exchange_class(config)
        else:
            self.client = exchange_class()
        self.log = Logger(self.__class__.__name__ + exchange_name)

    def fetch_balance(self, params={}):
        res = self.client.fetch_balance(params)
        # Clean up
        non_zero_coins = [c for c in res['total'] if res['total'][c] > 0]
        result = {
            "timestamp": res['timestamp'],
            "datetime": res['datetime'],
            "free": {},
            "used": {},
            "total": {},
        }
        for c in non_zero_coins:
            result["free"][c], result["used"][c], result["total"][c] = res[c]['free'], res[c]['used'], res[c]['total']
            result[c] = {'free': result["free"][c], 'used': result["used"][c], 'total': result["total"][c]}

        return result

    def get_price(self, symbol: str, params={}):
        res = self.client.fetch_ticker(symbol, params)
        return res['close']

    def fetch_order(self, id: str, symbol: str = None, params={}):
        return self.client.fetch_order(id, symbol, params)

    def fetch_orders(self, symbol: str = None, since: int = None, limit: int = None, params={}):
        return self.client.fetch_orders(symbol, since, limit, params)

    def cancel_order(self, id: str, symbol: str = None, params={}):
        self.client.cancel_order(id, symbol, params)

    def create_order(self, symbol: str, type: str, side: str, amount, price=None, params={}):
        return self.client.create_order(symbol, type, side, amount, price, params)

