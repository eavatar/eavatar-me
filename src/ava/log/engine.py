# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from .loghandler import QueueHandler

_logger = logging.getLogger(__name__)

_handler = QueueHandler()


def recent_log_entries():
    """
    :return: iterator for recent log entries.
    """
    global _handler

    return iter(_handler)


class LogEngine(object):

    def __init__(self):
        self._ctx = None
        _logger.debug("Log engine created.")

    def start(self, context):
        self._ctx = context
        root_logger = logging.getLogger()

        global _handler
        _handler = QueueHandler()
        root_logger.addHandler(_handler)
        # root_logger.setLevel(logging.INFO)
        _logger.debug("Log engine started.")

    def stop(self, context):
        global _handler

        _handler = None

        _logger.debug("Log engine stopped.")