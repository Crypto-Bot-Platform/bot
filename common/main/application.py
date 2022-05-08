import datetime
import yaml
from dependency_injector import containers, providers

arr = []
dic = {}


class Application(containers.DeclarativeContainer):
    with open('config.yml', 'r') as stream:

        try:
            config = yaml.safe_load(stream)
            bot_config = config['Bot']

            objects = {'Timer': providers.Singleton("common.time.time.Time",
                                                    start=(datetime.datetime.now() -
                                                           datetime.timedelta(
                                                               days=bot_config['Timer']['pastDays'])),
                                                    speed=bot_config['Timer']['speed'])}
            for adapter in bot_config['ExchangeAdapters']:
                exchange = providers.Factory(adapter['class'], exchange_name=adapter['name'], time=objects['Timer'])
                dic[adapter['name']] = exchange
                arr.append(exchange)

            objects['Exchanges'] = providers.Dict(dic)
            ExchangesList = providers.List(*arr)

            Validators = []
            for v in bot_config['Validators']:
                validator = providers.Singleton(v['class'], exchanges=ExchangesList)
                objects[v['name']] = validator
                Validators.append(validator)

            Validators = providers.List(*Validators)

            objects['OpenOrderManager'] = providers.Singleton(bot_config['OpenOrderManager']['class'],
                                                              exchanges=ExchangesList,
                                                              waiting_period=datetime.timedelta(
                                                                  seconds=bot_config['OpenOrderManager']['wait']),
                                                              portfolio=objects['PortfolioManager'],
                                                              time=objects['Timer'])

            objects['OrderManager'] = providers.Singleton('common.order.manager.OrderManager',
                                                          exchanges=ExchangesList,
                                                          open_order_mgr=objects['OpenOrderManager'])

            objects['OrderExecutor'] = providers.Singleton('common.order.executor.OrderExecutor',
                                                           validators=Validators,
                                                           order_manager=objects['OrderManager'])

            signalsParams = {}
            for p in bot_config['Signals']['params'] if 'params' in bot_config['Signals'] else []:
                for key,val in p.items():
                    signalsParams[key] = val if val[0] != '$' else objects[val[1:]]
            objects['Signals'] = providers.Singleton(bot_config['Signals']['class'], **signalsParams)

            strategyParams = {}
            for p in bot_config['Strategy']['params'] if 'params' in bot_config['Strategy'] else []:
                for key,val in p.items():
                    strategyParams[key] = val if val[0] != '$' else objects[val[1:]]
            objects['Strategy'] = providers.Singleton(bot_config['Strategy']['class'], **strategyParams)

            Objects = providers.Dict(objects)

        except yaml.YAMLError as exc:
            print(exc)
