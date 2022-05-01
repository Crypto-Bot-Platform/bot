from os import environ
from typing import List

from eslogger import Logger
from pymongo import MongoClient

from common.exchangeadapter.abstract import ExchangeAdapter
from common.openorder.manager import OpenOrderManager


class OrderManager:
    def __init__(self, exchanges: List[ExchangeAdapter], open_order_mgr: OpenOrderManager):
        self.exchanges = {}
        for exchange in exchanges:
            self.exchanges[exchange.exchangeName] = exchange

        self.oom = open_order_mgr
        elastic_host = environ['ELASTIC_HOST']
        elastic_port = environ['ELASTIC_PORT']
        mongo_host = environ['MONGODB_HOST'] if 'MONGODB_HOST' in environ else "localhost"
        mongo_port = environ['MONGODB_PORT'] if 'MONGODB_PORT' in environ else "27017"
        print(f"*** Environment variables: MONGODB_HOST={mongo_host}, MONGODB_PORT={mongo_port}, "
              f"ELASTIC_HOST={elastic_host}, ELASTIC_PORT={elastic_port}")
        self.db = MongoClient(host=mongo_host, port=int(mongo_port))
        self.bot_id = environ['BOT_ID'] if 'BOT_ID' in environ else "test-bot-01"
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

