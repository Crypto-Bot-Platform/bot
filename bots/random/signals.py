from common.signals.default import Signals


class MySignals(Signals):
    def calculate(self):
        return [
            {"name": "RSI", "value": self.indicators.RSI()},
            {"name": "Price", "value": self.indicators.price()}
        ]

