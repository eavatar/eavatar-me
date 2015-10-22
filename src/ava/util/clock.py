# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import time


class Clock(object):
    """ Logical timestamp generator.
    """
    def __init__(self, timestamp=None):
        if timestamp:
            self.l = (timestamp >> 16) & 0xffffffffffff
            self.c = timestamp & 0xffff
        else:
            self.l = 0
            self.c = 0
            self.tick()

    def update(self, rt=None):
        """ Updates the clock with a received timestamp from another node.

        :param rt: received timestamp
        """
        ml = (rt >> 16) & 0xffffffffffff
        mc = rt & 0xffff

        old_l = self.l
        pt = int(round((time.time() + 0.0005) * 1000.0))
        self.l = max(old_l, ml, pt)
        if self.l == old_l == ml:
            self.c = max(self.c, mc) + 1
        elif self.l == old_l:
            self.c += 1
        elif self.l == ml:
            self.c = mc + 1
        else:
            self.c = 0

    def tick(self):
        """ Updates and tick the clock for local or send events.

        :return: the updated timestamp
        """
        # local or send event
        old_l = self.l
        pt = int(round((time.time() + 0.0005) * 1000.0))
        self.l = max(old_l, pt)
        if self.l == old_l:
            self.c += 1
        else:
            self.c = 0

        return self.timestamp()

    def timestamp(self):
        """ Gets the current timestamp without updating counter.

        :return: the timestamp
        """
        return (self.l << 16) | self.c

    def seconds(self):
        """ Gets the value compatible with time.time() function.

        :return: the float value represent seconds from epoc
        """
        return (self.l/1000.0) + (self.c/65536.0)

    def __hash__(self):
        return self.timestamp()

    def __cmp__(self, other):
        if self.l != other.l:
            if self.l > other.l:
                return 1
            if self.l < other.l:
                return -1

        if self.c != other.c:
            if self.c > other.c:
                return 1
            if self.c < other.c:
                return -1
        return 0

    def __repr__(self):
        return "Clock[l=%r, c=%r]" % (self.l, self.c)

    @staticmethod
    def timestamp_to_secs(ts):
        """ Converts a timestamp to seconds.
        :param ts: the clock's timestamp.
        :return:
        """
        l = (ts >> 16) & 0xffffffffffff
        c = ts & 0xffff
        return (l/1000.0) + (c/65536.0)


clock = Clock()


__all__ = ['Clock', 'clock']
