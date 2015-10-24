# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
_logger = logging.getLogger(__name__)


class UserEngine(object):
    def __init__(self):
        self._context = None
        _logger.debug("User engine created.")

    def start(self, context):
        from avame import user
        self._context = context

