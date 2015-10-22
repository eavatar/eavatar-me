# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
from gevent import Greenlet

_logger = logging.getLogger(__name__)


class Scheduler(Greenlet):
    """ Scheduling tasks to run.
    """
    def __init__(self):
        super(Scheduler, self).__init__()

    def _run(self):
        pass
