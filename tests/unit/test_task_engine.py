# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import logging
import gevent
import unittest
from ava.task.engine import TaskEngine
from ava.core.context import Context
from ava.task import action
from ava.task import service

counter = 0


class TestTaskEngine(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.engine = TaskEngine()
        self.ctx = Context(None)
        self.ctx.bind('taskengine', self.engine)
        self.engine.start(self.ctx)
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        self.engine.stop(self.ctx)

    def test_register_and_unregister_action(self):

        def mock_action():
            return True

        t1 = self.engine.register(mock_action)
        action_key, mod_name, _ = service.action_key(__name__, 'mock_action')
        self.assertEqual(t1.key, action_key)

        self.engine.unregister(action_key)

        self.assertIsNone(self.engine.get_action(action_key))


class TestService(unittest.TestCase):

    def test_task_key(self):
        self.assertTrue(service.action_key('a', 'f'), 'a.f')
        self.assertTrue(service.action_key('b.a', 'f'), 'a.f')
        self.assertTrue(service.action_key('c.b.a', 'f'), 'a.f')
        self.assertTrue(service.action_key('a', 'f2'), 'a.f2')
