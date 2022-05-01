from common.strategy.default import Strategy


class MyStrategy(Strategy):
    def on(self, indicators):

        print(f"Received signal, {indicators}")

        if "RSI" in indicators and indicators['RSI'] > 70:
            print("BUY")

        if "RSI" in indicators and indicators['RSI'] < 20:
            print("SELL")



