from common.strategy.default import Strategy


class MyStrategy(Strategy):
    def on(self, indicators, context={}):
        exchange = context['exchange']
        pair = context['pair']
        [coin, base] = pair.split('/')
        print(f"Received signal, {indicators}. Context {context}")

        if "RSI" in indicators and indicators['RSI'] > 70:
            # BUY
            price = indicators['Price']
            balance = self.portfolio.get_available(exchange, base)
            amount_to_buy = 0.5 * balance/price
            self.order(exchange, pair, "buy", "market", amount_to_buy)

        if "RSI" in indicators and indicators['RSI'] < 30:
            # Sell
            balance = self.portfolio.get_available(exchange, coin)
            print(f"Available balance of {coin} is {balance}")
            self.order(exchange, pair, "sell", "market", balance)



