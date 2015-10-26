# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from ava.log.loghandler import QueueHandler


class TestLogHander(object):

    def test_info_logs_should_pass(self):

        logger = logging.getLogger("test1")

        handler = QueueHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        logger.info("msg1")
        logger.info("msg2")
        logger.info("msg3")
        assert len(handler.queue) == 3

    def test_debug_logs_should_be_filtered_out(self):
        logger = logging.getLogger("test1")

        handler = QueueHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.debug("msg1")
        logger.debug("msg2")
        logger.debug("msg3")

        assert len(handler.queue) == 0
