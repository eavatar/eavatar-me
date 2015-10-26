# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from datetime import datetime
from Queue import deque

from .defines import MAX_LEN_RECENT_ENTRIES


class QueueHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.setLevel(logging.INFO)

        self.queue = deque(maxlen=MAX_LEN_RECENT_ENTRIES)

    def __iter__(self):
        return iter(self.queue)

    def __len__(self):
        return len(self.queue)

    def emit(self, record):
        record.time = datetime.now()
        self.queue.appendleft(record)
