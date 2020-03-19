import sched
import sys
import os
import time
from app.bots.browse_page import browse_page


def recurring_browser(scheduler, interval, action, action_args=()):
    scheduler.enter(interval, 1, recurring_browser,
                    (scheduler, interval, action, action_args))
    action(*action_args)
    scheduler.run()


class PeriodicBrowser(object):
    """
        class will browse a page using "browse_page" function.

    """

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

    def start(self):
        self._running = True
        self.periodic(browse_page, actionargs=[self.address])
        self.scheduler.run()

    def stop(self):
        self._running = False
        if self.scheduler and self.event:
            self.scheduler.cancel(self.event)


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
