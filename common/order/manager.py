from typing import List

from eslogger import Logger
from pymongo import MongoClient

from common.exchangeadapter.abstract import ExchangeAdapter
from common.openorder.manager import OpenOrderManager
from common.utils.environment import parse_environ


class OrderManager:
    def __init__(self, exchanges: List[ExchangeAdapter], open_order_mgr: OpenOrderManager):
        self.exchanges = {}
        for exchange in exchanges:
            self.exchanges[exchange.exchangeName] = exchange

        self.oom = open_order_mgr
        params = parse_environ(self.__class__.__name__)
        elastic_host = params['elastic_host']
        elastic_port = params['elastic_port']
        mongo_host = params['mongo_host']
        mongo_port = params['mongo_port']
        self.db = MongoClient(host=mongo_host, port=int(mongo_port))
        self.bot_id = params['bot_id']
        self.log = Logger(f"{self.bot_id}:{self.__class__.__name__}", host=elastic_host, port=int(elastic_port))

    def execute(self, exchange_name: str, symbol: str, side: str, type: str, amount: float, price: float = None, params={}):
        # Set order
        order = self.exchanges[exchange_name].create_order(symbol, type, side, amount, price, params)
        # Record
        order['exchange'] = exchange_name
        collection = self.db['cbp']['orders']
        collection.update_one({'_id': order['id']}, {"$set": order}, upsert=True)
        # Monitor Order
        self.oom.start(exchange_name, symbol, order['id'])
        # Log
        self.log.info(f"Executing order: [Id:{order['id']}, Exchange:{exchange_name}, "
                      f"Symbol:{symbol}, Side:{side}, Type:{type}, Amount:{amount}, Price:{price}]")

