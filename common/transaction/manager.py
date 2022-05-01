from typing import List

from common.exchangeadapter.abstract import ExchangeAdapter


class TransactionManager:
    def __init__(self, exchanges: List[ExchangeAdapter]):
        self.exchanges = {}
        for exchange in exchanges:
            self.exchanges[exchange.exchangeName] = exchange

    def validate(self, exchange_name: str, symbol: str, side: str, type: str, amount: float, price: float = None, params={}) -> bool:
        (min_amount, max_amount) = self.exchanges[exchange_name].get_amount_limit(symbol)
        return min_amount <= amount <= max_amount
