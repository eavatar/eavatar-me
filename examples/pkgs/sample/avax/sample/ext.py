# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

logger = logging.getLogger(__name__)


class SampleExtension(object):
    """
    A sample extension for demonstrating how extension works.
    """

    def __init__(self):
        self.context = None
        logger.debug("Sample extension created.")

    def start(self, context):
        """Invoked to start the extension.

        :param context: the context object
        """
        self.context = context
        logger.debug("Sample extension started.")

    def stop(self, context):
        logger.debug("Sample extension stopped.")

