import datetime
import threading
from os import environ
from typing import List

from eslogger import Logger
from datetime import timedelta
from common.exchangeadapter.abstract import ExchangeAdapter
from common.time.time import Time


class OpenOrderManager:
    def __init__(self, exchanges: List[ExchangeAdapter], waiting_period: timedelta, time: Time = None):
        self.time = time if time else Time()
        elastic_host = environ['ELASTIC_HOST']
        elastic_port = environ['ELASTIC_PORT']
        self.bot_id = environ['BOT_ID'] if 'BOT_ID' in environ else "test-bot-01"
        print(f"*** Environment variables: ELASTIC_HOST={elastic_host}, ELASTIC_PORT={elastic_port}")
        self.log = Logger(f"{self.bot_id}:{self.__class__.__name__}", host=elastic_host, port=int(elastic_port))
        self.exchanges = {}
        for exchange in exchanges:
            self.exchanges[exchange.exchangeName] = exchange

        self.waiting_time = waiting_period

    def start(self, exchange_name: str, symbol: str, id: str):
        start_time = datetime.datetime.now()

        def execute():
            order = self.exchanges[exchange_name].fetch_order(id, symbol)
            while order['status'] != 'closed' and (start_time + self.waiting_time) > datetime.datetime.now():
                self.time.sleep(1)
                order = self.exchanges[exchange_name].fetch_order(id, symbol)
            if order['status'] == 'closed':
                self.log.info(f"Closed order: [Id:{order['id']}, Exchange:{exchange_name}, "
                              f"Symbol:{order['symbol']}, Side:{order['side']}, Type:{order['type']}, "
                              f"Amount:{order['amount']}, Price:{order['price']}]")
            elif (start_time + self.waiting_time) <= datetime.datetime.now():
                self.exchanges[exchange_name].cancel_order(order['id'])
                self.log.info(f"Canceling order {order['id']}, timeout...")

        threading.Thread(target=execute).start()

