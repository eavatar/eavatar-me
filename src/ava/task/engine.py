# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import gevent

from abc import abstractmethod
from uuid import uuid1
from gevent import Greenlet
from datetime import datetime

from . import TaskNotRegistered, TaskAlreadyRegistered
from . import service

_logger = logging.getLogger(__name__)


class ActionProxy(object):
    def __init__(self, task_engine, func, action_key):
        self.task_engine = task_engine
        self.func = func
        self.key = action_key

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class TaskRunner(Greenlet):
    """ Represent running tasks, each of which is an invocation to a procedure.
    """
    def __init__(self, task_id, action, args, kwargs):
        super(TaskRunner, self).__init__()
        self._task_id = task_id
        self._action = action
        self._args = args
        self._kwargs = kwargs

    @property
    def task_id(self):
        return self._task_id

    def _run(self):
        return self._action(*self._args, **self._kwargs)

    def done(self):
        """
        :return: True if the task was successfully executed or cancelled.
        """
        return self.ready()

    def result(self, timeout=None):
        try:
            if timeout:
                return self.get(block=True, timeout=timeout)
            else:
                return self.get()
        except Exception:
            raise

    def __hash__(self):
        return hash(self._task_id)

    def __eq__(self, other):
        return self.task_id == other.task_id


class TaskEngine(object):

    def __init__(self):
        self.context = None
        self._schedules = {}
        self._actions = {}
        self._tasks = {}

    def start(self, ctx):
        _logger.debug("Starting task engine...")
        self.context = ctx
        self.context['taskengine'] = self

    def stop(self, ctx):
        _logger.debug("Stopping task engine...")
        for sched in self._schedules.values():
            sched.kill()
        gevent.joinall(self._schedules.values())

    def register(self, func):
        action_key = service.action_key(func.__module__, func.func_name)

        if self._actions.get(action_key) is not None:
            raise TaskAlreadyRegistered(action_key)

        _logger.debug("Action %s registered." % action_key)
        proxy = ActionProxy(self, func, action_key)
        self._actions[action_key] = proxy
        return proxy

    def unregister(self, task_key):
        proxy = self._actions.get(task_key)
        if proxy is not None:
            del self._actions[task_key]

    def get_action(self, action_key):
        return self._actions.get(action_key)

    def do_task(self, action_key, *args, **kwargs):
        action = self._actions[action_key]
        task_id = uuid1().hex
        task = TaskRunner(task_id, action, args, kwargs)
        self._tasks[task_id] = task
        task.start()
        return task

