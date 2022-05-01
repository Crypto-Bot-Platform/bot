import datetime

import yaml
from dependency_injector import containers, providers


class Application(containers.DeclarativeContainer):
    with open('config.yml', 'r') as stream:
        try:
            config = yaml.safe_load(stream)

            signals = providers.Factory(config['Bot']['Signals']['class'],
                                        exchange=config['Bot']['Signals']['params'][0]['exchange'],
                                        pair=config['Bot']['Signals']['params'][0]['pair'])
            strategy = providers.Factory(config['Bot']['Strategy']['class'])

            time = providers.Factory(config['Bot']['Timer']['class'],
                                     start=(datetime.datetime.now() -
                                            datetime.timedelta(
                                                days=config['Bot']['Timer']['params'][0]['pastDays'])),
                                     speed=config['Bot']['Timer']['params'][0]['speed'])

        except yaml.YAMLError as exc:
            print(exc)
