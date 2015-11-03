# -*- coding: utf-8 -*-

import os
import unittest

from ava.runtime import environ


class TestRuntimeConfig(unittest.TestCase):

    def setUp(self):
        from ava import wrapper
        wrapper.init_app_dir()

    def test_should_have_dir_settings(self):
        from ava.runtime.config import settings
        self.assertIsNotNone(settings.get('conf_dir'))
        self.assertIsNotNone(settings.get('data_dir'))
        self.assertIsNotNone(settings.get('logs_dir'))

    def test_should_have_logging_settings(self):
        from ava.runtime.config import settings
        handlers = settings['LOGGING']['handlers']
        self.assertIsNotNone(handlers)
        log_file = handlers['file_handler']['filename']
        #print(log_file)
        self.assertIsNotNone(log_file)


class TestRuntimeEnviron(unittest.TestCase):

    def setUp(self):
        from ava import wrapper
        wrapper.init_app_dir()

    def test_work_home(self):
        env = environ.Environment()
        self.assertTrue(os.path.isdir(env.pod_dir))
        print(env.conf_dir)
        self.assertTrue(os.path.isdir(env.conf_dir))
        self.assertTrue(os.path.isdir(env.data_dir))
        self.assertTrue(os.path.isdir(env.logs_dir))

