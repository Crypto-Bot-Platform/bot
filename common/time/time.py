import datetime
import time


class Time:
    def __init__(self, start: datetime.datetime = None, speed: int = 1):
        self.delta = datetime.datetime.now() - start if start is not None else datetime.timedelta(seconds=0)
        self.speed = speed

    def now(self):
        return (datetime.datetime.now() - self.delta) if self.delta.total_seconds() > 0 else datetime.datetime.now()

    def sleep(self, seconds: float):
        period_delta = seconds - (seconds/self.speed)
        self.delta -= datetime.timedelta(seconds=period_delta)
        time.sleep(seconds/self.speed)
        if self.delta < datetime.timedelta(seconds=0):
            self.delta = datetime.timedelta(seconds=0)
            self.speed = 1


if __name__ == "__main__":
    t = Time(datetime.datetime.now() - datetime.timedelta(hours=1), 100)
    # t = Time()
    while True:
        print(t.now())
        t.sleep(10)