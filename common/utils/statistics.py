import threading
from datetime import datetime

from common.utils.environment import parse_environ
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class StatisticsRecorder:
    def __init__(self):
        params = parse_environ(self.__class__.__name__)
        elastic_host = params['elastic_host']
        elastic_port = params['elastic_port']
        self.bot_id = params['bot_id']
        self.es = Elasticsearch(hosts=elastic_host, port=int(elastic_port))

    def async_post_portfolio(self, portfolio):
        def post():
            actions = [
                {
                    "_index": "bot-statistics",
                    "_source": {
                        "@timestamp": datetime.utcnow(),
                        "bot_id": self.bot_id,
                        "type": "balance",
                        "exchange": exchange,
                        "coin": coin,
                        "free": portfolio[exchange]['free'][coin] if coin in portfolio[exchange]['free'] else 0,
                        "used": portfolio[exchange]['used'][coin] if coin in portfolio[exchange]['used'] else 0,
                        "total": portfolio[exchange]['total'][coin] if coin in portfolio[exchange]['total'] else 0,
                    }
                } for exchange in portfolio for coin in portfolio[exchange]['total']
            ]
            bulk(self.es, actions)
        threading.Thread(target=post, args=()).start()

    def post_health_check(self):
        self.es.index(index="bot-statistics", doc_type="_doc", document={
                "@timestamp": datetime.utcnow(),
                "bot_id": self.bot_id,
                "type": "health",
        })

    def post_order(self, order):
        doc = {
            "@timestamp": datetime.utcnow(),
            "bot_id": self.bot_id,
            "type": "order",
        }
        order.update(doc)
        if '_id' in order:
            del order['_id']
        self.es.index(index="bot-statistics", doc_type="_doc", document=order)

