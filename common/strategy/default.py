import collections
import threading
from datetime import datetime

import events
from eslogger import Logger

from common.schema.signals import SignalsSchema


class Strategy:
    def __init__(self):
        self.log = Logger(self.__class__.__name__)
        self.address = None
        self.em = events.EventManager()

    def on(self, indicators):
        raise NotImplemented()

    def init(self, bot_id: str):
        self.address = f"{bot_id}-strategy"
        self.em.create_address(self.address)

    def handle(self, data):
        res = collections.defaultdict(float)
        print(str(datetime.fromtimestamp(data['timestamp'] / 1000)))
        for indicator in data["indicators"]:
            res[indicator['name']] = indicator['value']
        self.on(res)

    def listen(self):
        threading.Thread(target=self.em.wait_for_command, args=(self.address, SignalsSchema, self.handle)).start()



