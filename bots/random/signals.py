from common.signals.default import Signals


class MySignals(Signals):
    def __init__(self, exchange: str, pair: str):
        super().__init__(exchange, pair)

    def calculate(self):
        return [
            {"name": "RSI", "value": self.indicators.RSI()}
        ]

