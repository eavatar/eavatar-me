# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from ava.data import get_store
from ava.util.clock import clock

from .signals import USER_NOTIFIED
from .models import Notice

_logger = logging.getLogger(__name__)


class UserEngine(object):
    def __init__(self):
        self._context = None
        self._notice_store = None
        _logger.debug("User engine created.")

    def start(self, context):
        self._context = context
        context.connect(self.on_user_notified, signal=USER_NOTIFIED)
        self._notice_store = get_store('notices')

    def stop(self, context):
        _logger.debug("User engine stopped.")

    def on_user_notified(self, msg, title):
        try:
            notice = Notice(message=msg, title=title)
            self._notice_store[notice.id] = [notice.to_dict(), clock.tick()]
            _logger.debug("User notice saved: %s", notice.id)
        except Exception:
            _logger.error("Failed to save notice to store.", exc_info=True)
