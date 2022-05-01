import threading
import uuid

from dependency_injector.wiring import Provide, inject
from application import Application


from common.signals.default import Signals
from common.strategy.default import Strategy
from common.time.time import Time


@inject
def main(
        signals: Signals = Provide[Application.signals],
        strategy: Strategy = Provide[Application.strategy],
        time: Time = Provide[Application.time]
) -> None:
    config = Application.config
    bot_id = str(uuid.uuid4())
    signals.init(bot_id, time)
    strategy.init(bot_id)

    threading.Thread(target=signals.run, args=(config['Bot']['Sleep'],)).start()
    threading.Thread(target=strategy.listen).start()


if __name__ == "__main__":
    container = Application()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
