import datetime
import time
import uuid
from os import environ

import psycopg2
from pymongo import MongoClient

from common.exchangeadapter.abstract import ExchangeAdapter
from eslogger import Logger

from common.time.time import Time


class MockExchangeAdapter(ExchangeAdapter):
    def __init__(self, exchange_name: str, time: Time = None, config=None):
        super().__init__(exchange_name)
        self.name = exchange_name
        self.log = Logger(self.__class__.__name__ + exchange_name)
        self.time = time if time else Time()
        self.bot_id = environ['BOT_ID'] if 'BOT_ID' in environ else "test-bot-01"
        mongo_host = environ['MONGODB_HOST'] if 'MONGODB_HOST' in environ else "localhost"
        mongo_port = environ['MONGODB_PORT'] if 'MONGODB_PORT' in environ else "27017"
        db_name = environ['SQLDB_NAME']
        db_user = environ['SQLDB_USER']
        db_pass = environ['SQLDB_PASS']
        db_host = environ['SQLDB_HOST']
        db_port = int(environ['SQLDB_PORT'])
        print(f"*** Environment variables: SQLDB_HOST={db_host}, SQLDB_PORT={db_port}, SQLDB_NAME = {db_name},"
              f"SQLDB_USER={db_user}, SQLDB_PASS={db_pass}, BOT_ID={self.bot_id}, MONGODB_HOST={mongo_host}, "
              f"MONGODB_PORT={mongo_port}")
        self.conn = psycopg2.connect(f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
        self.db_client = MongoClient(host=mongo_host, port=int(mongo_port))

    def fetch_balance(self, params={}):
        collection = self.db_client['mock']['balance']
        balance = collection.find_one({"_id": self.bot_id})
        if not balance:
            # Create Empty one and store it in DB
            balance = {
                "timestamp": time.time(),
                "datetime": datetime.datetime.now(),
                "free": {},
                "used": {},
                "total": {},
            }
            collection.update_one({'_id': self.bot_id}, {"$set": balance}, upsert=True)
        return balance

    def get_price(self, symbol: str, params={}) -> float:
        c = self.conn.cursor()
        try:
            c.execute(f"""
                    select closing_price
                    from ticks
                    where exchange = '{self.name}' and pair = '{symbol}' and time < '{self.time.now()}'
                    order by time desc
                    limit 1 
                    """)
            data = c.fetchone()
            return data[0]
        except (Exception, psycopg2.Error) as error:
            self.log.error(error.pgerror)

    def create_order(self, symbol: str, type: str, side: str, amount, price=None, params={}):
        [coin, base] = symbol.split('/')
        # Always successful order
        collection = self.db_client['mock']['orders']
        price = self.get_price(symbol)
        id = uuid.uuid4()
        # TODO:
        #   - Handle 'limit' and 'market' order differently
        #   - Identify fee/cost and fee/rate values
        order = {
            'id': str(id),
            'clientId': self.bot_id,
            'datetime': self.time.now(),
            'timestamp': self.time.now().timestamp() * 1e3,
            'status': 'closed',  # Close transaction immediately
            'symbol': symbol,
            'type': type,
            'timeInForce': 'GTC',
            'side': side,
            'price': price,
            'average': price,
            'amount': amount,
            'filled': amount,
            'remaining': 0,
            'cost': amount * price,
            'fee': {
                'currency': symbol.split('/')[1],
                'cost': self.get_taker_fee(symbol),
                'rate': 0
            }
        }
        collection.update_one({'_id': str(id)}, {"$set": order}, upsert=True)
        collection = self.db_client['mock']['balance']
        balance = collection.find_one({"_id": self.bot_id})
        if side == "buy":
            # Buy
            balance['free'][coin] = balance['free'][coin] + amount if coin in balance['free'] else amount
            balance['total'][coin] = balance['total'][coin] + amount if coin in balance['total'] else amount

            cost = amount * price * (1+float(order['fee']['cost']))
            balance['free'][base] = balance['free'][base] - cost if base in balance['free'] else 0 - cost
            balance['total'][base] = balance['total'][base] - cost if base in balance['total'] else 0 - cost

        else:
            # Sell
            balance['free'][coin] = balance['free'][coin] - amount if coin in balance['free'] else 0 - amount
            balance['total'][coin] = balance['total'][coin] - amount if coin in balance['total'] else 0 - amount

            cost = amount * price * (1 - float(order['fee']['cost']))
            balance['free'][base] = balance['free'][base] + cost if base in balance['free'] else cost
            balance['total'][base] = balance['total'][base] + cost if base in balance['total'] else cost

        balance[coin] = {
            "free": balance['free'][coin],
            "used": 0,
            "total": balance['total'][coin]
        }
        balance[base] = {
            "free": balance['free'][base],
            "used": 0,
            "total": balance['total'][base]
        }
        collection.update_one({'_id': self.bot_id}, {"$set": balance}, upsert=True)
        return order

    def cancel_order(self, id: str, symbol: str = None, params={}):
        return

    def fetch_orders(self, symbol: str = None, since: int = None, limit: int = None, params={}):
        collection = self.db_client['mock']['orders']
        search_filter = {
            "clientId": self.bot_id,
            "timestamp": {"$lt": since if since is not None else self.time.now().timestamp() * 1e3}
        }
        if symbol:
            search_filter['symbol'] = symbol
        result = []
        for doc in collection.find(search_filter).limit(limit if limit else 100):
            result.append(doc)

        return result

    def fetch_order(self, id: str, symbol: str = None, params={}):
        collection = self.db_client['mock']['orders']
        return collection.find_one({"_id": id})

