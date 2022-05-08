from typing import List

from common.exchangeadapter.abstract import ExchangeAdapter
from common.order.validator import OrderValidator


class PortfolioManager(OrderValidator):

    def __init__(self, exchanges: List[ExchangeAdapter]):
        self.exchanges = {}
        self.balance = {}
        for exchange in exchanges:
            self.exchanges[exchange.exchangeName] = exchange
            self.balance[exchange.exchangeName] = exchange.fetch_balance()

    def sync(self, exchange_name: str):
        exchange = self.exchanges[exchange_name]
        self.balance[exchange.exchangeName] = exchange.fetch_balance()

    def get_available(self, exchange_name: str, coin: str) -> float:
        if exchange_name in self.balance and coin in self.balance[exchange_name]:
            free = self.balance[exchange_name][coin]['free']
            return float(free)

        return 0

    def validate(self, exchange_name: str, symbol: str, side: str, type: str, amount: float, price: float = None, params={}) -> bool:
        [coin, base] = symbol.split('/')
        exchange = self.exchanges[exchange_name]
        if side == 'buy':
            # Buy
            if type == 'limit':
                # Limit
                required_base = price * amount * (1+exchange.get_maker_fee(symbol))
                return self.balance[exchange_name][base]['free'] >= required_base if base in self.balance[exchange_name] else False
            else:
                # Market
                required_base = exchange.get_price(symbol) * amount * (1+exchange.get_maker_fee(symbol))
                return self.balance[exchange_name][base]['free'] >= required_base if base in self.balance[exchange_name] else False
        else:
            # Sell
            return self.balance[exchange_name][coin]['free'] >= amount if coin in self.balance[exchange_name] else False
