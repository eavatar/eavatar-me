# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import datetime
import time


class Schedule(object):
    """
    For simple recurring-interval scheduling.

    Eg. the loop body would be run roughly every 1 hour.

    >>> for it in Schedule().every(1).hour:
            ...

    """

    _SECONDS = 1
    _MINUTES = 2
    _HOURS = 3
    _DAYS = 4

    def __init__(self):
        self._delayed = 0
        self._interval = 1
        self._unit = self._MINUTES
        self._count = 0
        self._total_count = None
        self._next_run = None
        self._last_run = None

    def every(self, interval=1):
        self._interval = interval
        return self

    def counts(self, c):
        assert c >= 1
        self._total_count = c
        return self

    @property
    def second(self):
        assert self._interval == 1
        self._unit = self._SECONDS
        return self

    @property
    def seconds(self):
        self._unit = self._SECONDS
        return self

    @property
    def minute(self):
        assert self._interval == 1
        self._unit = self._MINUTES
        return self

    @property
    def minutes(self):
        self._unit = self._MINUTES
        return self

    @property
    def hour(self):
        assert self._interval == 1
        self._unit = self._HOURS
        return self

    @property
    def hours(self):
        self._unit = self._HOURS
        return self

    @property
    def day(self):
        assert self._interval == 1
        self._unit = self._DAYS
        return self

    @property
    def days(self):
        self._unit = self._DAYS
        return self

    def next_time_delta(self):
        period = 60
        if self._unit == self._SECONDS:
            period = datetime.timedelta(seconds=self._interval)
        elif self._unit == self._MINUTES:
            period = datetime.timedelta(minutes=self._interval)
        elif self._unit == self._HOURS:
            period = datetime.timedelta(hours=self._interval)
        elif self._unit == self._DAYS:
            period = datetime.timedelta(days=self._interval)

        return period

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self._total_count and self._count >= self._total_count:
            raise StopIteration()

        period = self.next_time_delta()
        self._next_run = datetime.datetime.now() + period

        time.sleep(period.seconds)
        self._last_run = self._next_run

        self._count += 1

        return self._count


def schedule():
    return Schedule()
