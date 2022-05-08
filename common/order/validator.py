class OrderValidator:
    def validate(self, exchange_name: str, symbol: str, side: str, type: str, amount: float, price: float = None,
                 params={}) -> bool:
        raise NotImplemented()