import math
import threading
import time
from typing import List

import events
from eslogger import Logger

from common.order.manager import OrderManager
from common.order.validator import OrderValidator
from common.schema.executor import ExecutorSchema
from common.utils.environment import parse_environ

lock = threading.Lock()


class OrderExecutor:
    def __init__(self, validators: List[OrderValidator], order_manager: OrderManager):
        self.validators = validators
        self.in_progress = False
        params = parse_environ(self.__class__.__name__)
        self.bot_id = params['bot_id']
        kafka_host = params['kafka_host']
        kafka_port = params['kafka_port']
        elastic_host = params['elastic_host']
        elastic_port = params['elastic_port']
        self.em = events.EventManager(kafka_host, int(kafka_port))
        self.om = order_manager
        self.address = f"{self.bot_id}-executor"
        self.em.create_address(self.address)
        self.log = Logger(self.__class__.__name__ + self.bot_id, host=elastic_host, port=int(elastic_port))

    def handle(self, data):
        def truncate(num, n):
            integer = math.floor(num * (10 ** n)) / (10 ** n)
            return float(integer)

        lock.acquire()
        try:
            print(f"*** In Handle request. Data: {data}")
            # Handle execute request
            exchange, symbol, side, type, amount, price = \
                data['exchange'], data['symbol'], data['side'], data['type'], truncate(data['amount'], 4), data['price']

            # Validate first
            for validator in self.validators:
                if not validator.validate(exchange, symbol, side, type, amount, price):
                    self.log.info(f"Order didn't pass validation. Validator[{validator.__class__.__name__}]",
                                  {"exchange": exchange, "symbol": symbol, "side": side, "amount": amount, "price": price,
                                   "bot_id": self.bot_id})
                    print(f"*** Didn't pass validation. Data: {data}")
                    return

            # Execute
            self.log.info(f"Start executing order",
                          {"exchange": exchange, "symbol": symbol, "side": side, "amount": amount, "price": price,
                           "bot_id": self.bot_id})
            self.om.execute(exchange, symbol, side, type, amount, price)
        finally:
            print(f"*** Finishing handling request. Data: {data}")
            lock.release()

    def listen(self):
        threading.Thread(target=self.em.wait_for_command, args=(self.address, ExecutorSchema, self.handle)).start()
