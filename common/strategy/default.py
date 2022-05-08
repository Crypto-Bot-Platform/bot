import collections
import threading
from datetime import datetime

import events
from eslogger import Logger

from common.portfolio.manager import PortfolioManager
from common.schema.executor import ExecutorSchema
from common.schema.signals import SignalsSchema
from common.utils.environment import parse_environ


class Strategy:
    def __init__(self, portfolio: PortfolioManager, exchange: str):
        params = parse_environ(self.__class__.__name__)
        kafka_host = params['kafka_host']
        kafka_port = params['kafka_port']
        elastic_host = params['elastic_host']
        elastic_port = params['elastic_port']
        self.bot_id = params['bot_id']
        self.em = events.EventManager(host=kafka_host, port=int(kafka_port))
        self.log = Logger(f"{self.bot_id}/{self.__class__.__name__}", host=elastic_host, port=int(elastic_port))
        self.address = f"{self.bot_id}-strategy"
        self.em.create_address(self.address)
        self.portfolio = portfolio
        self.exchange = exchange

    def on(self, indicators, context={}):
        raise NotImplemented()

    def handle(self, data):
        res = collections.defaultdict(float)
        print(str(datetime.fromtimestamp(data['timestamp'] / 1000)))
        for indicator in data["indicators"]:
            res[indicator['name']] = indicator['value']
        self.on(res, data["context"])

    def order(self, exchange: str, symbol: str, side: str, type: str, amount: float, price: float=0):
        self.em.send_command_to_address(f"{self.bot_id}-executor", ExecutorSchema, {
            "timestamp": int(datetime.now().timestamp() * 1000),
            "exchange": exchange,
            "symbol": symbol,
            "side": side,
            "type": type,
            "amount": amount,
            "price": price
        })

    def listen(self):
        threading.Thread(target=self.em.wait_for_command, args=(self.address, SignalsSchema, self.handle)).start()
