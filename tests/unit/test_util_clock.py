# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import time
from ava.util.clock import Clock

import pytest

@pytest.fixture
def clock():
    return Clock()


class TestClock(object):

    def test_milliseconds_round_up(self):
        t = time.time()
        pt = round((t + 0.0005), 3)
        assert pt >= t

    def test_clock_should_increment_monotonically(self, clock):
        prev = clock.timestamp()
        for _ in xrange(2000):
            cur = clock.tick()
            # print('%r' % cur)
            assert cur > prev
            prev = cur

    def test_create_clock_from_timestamp(self):
        c = Clock(94132454961709074)
        assert c.l == 1436347274196
        assert c.c == 18

    def test_clock_seconds_should_be_bounded(self):
        c = Clock().seconds()
        t = time.time()
        assert (c - t) < 0.002

    def test_clock_tick_with_timestamp(self, monkeypatch):
        def mytime():
            return 1436345964.484081
        monkeypatch.setattr(time, 'time', mytime)
        # print(time.time())
        c = Clock(94132454961709074)
        assert c.l == 1436347274196
        assert c.c == 18
        c.update(94132454961709075)
        assert c.c == 20  # tick() increments c by 1 as well


if __name__ == '__main__':
    clock = Clock()
    for i in range(100):
        clock.tick()
        print("%r, %r" % (clock.timestamp(), time.time()))
        time.sleep(0.1)
