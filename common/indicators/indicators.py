import psycopg2
from eslogger import Logger

from common.time.time import Time
from common.utils.environment import parse_environ


class Indicators:
    def __init__(self, exchange: str, pair: str, timer: Time = None):
        self.exchange = exchange
        self.pair = pair
        self.timer = timer if timer is not None else Time()
        params = parse_environ(self.__class__.__name__)
        db_name = params['db_name']
        db_user = params['db_user']
        db_pass = params['db_pass']
        db_host = params['db_host']
        db_port = int(params['db_port'])
        self.bot_id = params['bot_id']
        self.conn = psycopg2.connect(f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")
        self.log = Logger(f"{self.bot_id}/{self.__class__.__name__}")

    def RSI(self):
        c = self.conn.cursor()
        try:
            c.execute(f"""
            SELECT value1 
            FROM indicators
            WHERE exchange = '{self.exchange}' and 
                  pair = '{self.pair}' and 
                  name = 'RSI' and 
                  time <= '{self.timer.now()}' 
            ORDER BY time DESC
            """)
            value = c.fetchone()
            return value[0]
        except Exception as e:
            self.log.error(e)

    def price(self):
        c = self.conn.cursor()
        try:
            c.execute(f"""
                    SELECT closing_price 
                    FROM ticks
                    WHERE exchange = '{self.exchange}' and 
                          pair = '{self.pair}' and
                          time <= '{self.timer.now()}' 
                    ORDER BY time DESC
                    LIMIT 1
                    """)
            value = c.fetchone()
            return value[0]
        except Exception as e:
            self.log.error(e)


