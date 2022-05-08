import threading

from dependency_injector.wiring import Provide, inject
from application import Application

@inject
def main(
        objects = Provide[Application.Objects]
) -> None:
    config = Application.config
    time = objects['Timer']
    strategy = objects['Strategy']
    signals = objects['Signals']
    order_executor = objects['OrderExecutor']
    signals.init(time)

    order_executor.listen()
    threading.Thread(target=signals.run, args=(config['Bot']['Config']['Sleep'],)).start()
    threading.Thread(target=strategy.listen).start()


if __name__ == "__main__":
    container = Application()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
