import sched
import sys
import os
import time


class PeriodicFunction(object):
    def __init__(self, interval, address):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.interval = interval
        self.address = address
        self._running = False

    def periodic(self, action, actionargs=()):
        if self._running:
            self.event = self.scheduler.enter(
                self.interval, 1, self.periodic, (action, actionargs))
            action(*actionargs)

    def start(self, periodic_function):
        self._running = True
        self.periodic(periodic_function, actionargs=[self.address])
        self.scheduler.run()

    def stop(self):
        self._running = False
        if self.scheduler and self.event:
            self.scheduler.cancel(self.event)
