import datetime

import events
from eslogger import Logger

from common.indicators.indicators import Indicators
from common.schema.signals import SignalsSchema
from common.time.time import Time
from common.utils.environment import parse_environ


class Signals:
    def __init__(self, exchange: str, pair: str):
        params = parse_environ(self.__class__.__name__)
        bot_id = params['bot_id']
        kafka_host = params['kafka_host']
        kafka_port = params['kafka_port']
        elastic_host = params['elastic_host']
        elastic_port = params['elastic_port']
        self.exchange = exchange
        self.pair = pair
        self.bot_id = bot_id
        self.indicators = None
        self.timer = None
        self.em = events.EventManager(host=kafka_host, port=int(kafka_port))
        self.log = Logger(f"{self.bot_id}/{self.__class__.__name__}", host=elastic_host, port=int(elastic_port))

    def calculate(self):
        raise NotImplemented()

    def init(self, timer: Time = None):
        self.timer = timer if timer is not None else Time()
        self.indicators = Indicators(self.exchange, self.pair, timer)

    def run(self, sleep=1):
        while True:
            try:
                data = self.calculate()
                self.em.send_command_to_address(f"{self.bot_id}-strategy", SignalsSchema, {
                    "timestamp": int(self.timer.now().timestamp() * 1000),
                    "indicators": data,
                    "context": {
                        "exchange": self.exchange,
                        "pair": self.pair,
                    }
                })
                self.timer.sleep(sleep)
            except Exception as e:
                self.log.error("Failed to send signal:", str(e))
