import psycopg2
from eslogger import Logger

from common.time.time import Time


class Indicators:
    def __init__(self, exchange: str, pair: str, timer: Time = None):
        self.log = Logger(self.__class__.__name__)
        self.exchange = exchange
        self.pair = pair
        self.timer = timer if timer is not None else Time()
        # TODO: Use config file
        db_name = "cbp"
        db_user = "cbp_user"
        db_pass = "Password1234"
        db_host = "10.0.0.212"
        db_port = 5432
        self.conn = psycopg2.connect(f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

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


i = Indicators('ftx', 'BTC/USDT')
print(i.RSI())
