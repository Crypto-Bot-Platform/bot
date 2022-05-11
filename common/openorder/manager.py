import datetime
import threading
from typing import List

from eslogger import Logger
from datetime import timedelta
from common.exchangeadapter.abstract import ExchangeAdapter
from common.portfolio.manager import PortfolioManager
from common.time.time import Time
from common.utils.environment import parse_environ
from common.utils.statistics import StatisticsRecorder


class OpenOrderManager:
    def __init__(self, exchanges: List[ExchangeAdapter], waiting_period: timedelta, portfolio: PortfolioManager, time: Time = None):
        self.time = time if time else Time()
        self.portfolio = portfolio
        params = parse_environ(self.__class__.__name__)
        elastic_host = params['elastic_host']
        elastic_port = params['elastic_port']
        self.bot_id = params['bot_id']
        self.log = Logger(f"{self.bot_id}/{self.__class__.__name__}", host=elastic_host, port=int(elastic_port))
        self.exchanges = {}
        for exchange in exchanges:
            self.exchanges[exchange.exchangeName] = exchange

        self.waiting_time = waiting_period
        self.sr = StatisticsRecorder()

    def start(self, exchange_name: str, symbol: str, id: str):
        start_time = datetime.datetime.now()
        self.portfolio.sync(exchange_name)

        def execute():
            order = self.exchanges[exchange_name].fetch_order(id, symbol)
            while order['status'] != 'closed' and (start_time + self.waiting_time) > datetime.datetime.now():
                self.sr.post_order(order)
                self.time.sleep(1)
                order = self.exchanges[exchange_name].fetch_order(id, symbol)

            if order['status'] == 'closed':
                self.log.info(f"Closed order: [Id:{order['id']}, Exchange:{exchange_name}, "
                              f"Symbol:{order['symbol']}, Side:{order['side']}, Type:{order['type']}, "
                              f"Amount:{order['amount']}, Price:{order['price']}]")
                self.sr.post_order(order)
            elif (start_time + self.waiting_time) <= datetime.datetime.now():
                order['status'] = 'cancel'
                self.sr.post_order(order)
                self.exchanges[exchange_name].cancel_order(order['id'])
                self.log.info(f"Canceling order {order['id']}, timeout...")
            self.portfolio.sync(exchange_name)
        threading.Thread(target=execute).start()

