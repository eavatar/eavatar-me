# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

"""
Support for functional tests
"""

import os
import unittest
import gevent
import shutil
import tempfile
import pytest
import logging

from ava.core.defines import AVA_SWARM_SECRET, AVA_AGENT_SECRET
from ava.util import base_path, defines
from ava.core import context, agent_running, agent_stopped

from gevent import monkey
monkey.patch_all(thread=False)

_logger = logging.getLogger(__name__)


def prepare_agent_test_env():
    """
    Constructs the skeleton of directories if it not there already.
    :return:
    """
    pod_folder = tempfile.mkdtemp()
    if defines.POD_ENV_NAME in os.environ:
        del os.environ[defines.POD_ENV_NAME]
    os.environ.setdefault(defines.POD_ENV_NAME, pod_folder)
    assert os.path.exists(pod_folder)
    from ava.runtime import environ
    environ.get_environ(reset=True)

    base_dir = base_path()

    src_dir = os.path.join(base_dir, defines.POD_FOLDER_NAME)

    # copy files from base_dir to user_dir
    subdirs = os.listdir(src_dir)
    for d in subdirs:
        src_path = os.path.join(src_dir, d)
        dst_path = os.path.join(pod_folder, d)
        ignore_pattern = shutil.ignore_patterns("__init__.py")

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, ignore=ignore_pattern)
        else:
            shutil.copy2(src_path, dst_path)

    return pod_folder

user_xid = b'AYPwK3c3VK7ZdBvKfcbV5EmmCZ8zSb9viZ288gKFBFuE92jE'
user_key = b'Kd2xqKsjTnhhqXjY64eeSEyS1i9kSGTHt9S57sqeK51bkPRh'
swarm_secret = b'SVQh1mgbdvuFoZihYH8urZyBGpfZ4PJnn8af2R9MuqZyktHa'

agent_secret = b'SYNmgyQqhAnVwKLrmSmYzahkzH3V51qdShL41JFPnmsZob96'


class AgentTest(unittest.TestCase):
    """
    For functional tests which require a running agent.
    """
    agent = None
    pod_folder = None

    @classmethod
    def setUpClass(cls):
        cls.pod_folder = prepare_agent_test_env()
        _logger.info("Temp POD folder: %s", cls.pod_folder)

        from ava.runtime.config import settings
        from ava.core.agent import Agent

        settings['DEBUG'] = True
        settings['TEST'] = True
        os.environ.setdefault(AVA_SWARM_SECRET, swarm_secret)
        os.environ.setdefault(AVA_AGENT_SECRET, agent_secret)
        AgentTest.agent = Agent(None, None)
        gevent.spawn(AgentTest.agent.run)
        agent_running.wait(10)

    @classmethod
    def tearDownClass(cls):
        AgentTest.agent.interrupted = True
        agent_stopped.wait(10)
        context._context = None
        shutil.rmtree(cls.pod_folder)
        _logger.info("Temp POD folder removed: %s", cls.pod_folder)


@pytest.fixture(scope='session')
def agent(request):
    from ava.runtime.config import settings
    from ava.core.agent import Agent

    pod_folder = prepare_agent_test_env()
    settings['GENERAL']['TEST'] = True
    os.environ.setdefault(AVA_SWARM_SECRET, swarm_secret)
    os.environ.setdefault(AVA_AGENT_SECRET, agent_secret)
    _agent = Agent(None, None)
    gevent.spawn(_agent.run)
    agent_running.wait(10)

    def teardown_agent():
        if not agent:
            return
        _agent.interrupted = True
        agent_stopped.wait(10)
        shutil.rmtree(pod_folder)

    request.addfinalizer(teardown_agent)
    return _agent
