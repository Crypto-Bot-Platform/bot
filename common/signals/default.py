import datetime

import events
from eslogger import Logger

from common.indicators.indicators import Indicators
from common.schema.signals import SignalsSchema
from common.time.time import Time


class Signals:
    def __init__(self, exchange: str, pair: str):
        self.log = Logger(self.__class__.__name__)
        self.exchange = exchange
        self.pair = pair
        self.indicators = None
        self.bot_id = None
        self.timer = None
        self.em = events.EventManager()

    def calculate(self):
        raise NotImplemented()

    def init(self, bot_id: str, timer: Time = None):
        self.bot_id = bot_id
        self.timer = timer if timer is not None else Time()
        self.indicators = Indicators(self.exchange, self.pair, timer)

    def run(self, sleep=1):
        while True:
            try:
                data = self.calculate()
                self.em.send_command_to_address(f"{self.bot_id}-strategy", SignalsSchema, {
                    "timestamp": int(self.timer.now().timestamp() * 1000),
                    "indicators": data
                })
                self.timer.sleep(sleep)
            except Exception as e:
                self.log.error("Failed to send signal:", str(e))
