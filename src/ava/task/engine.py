# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import gevent

from gevent import Greenlet

from ..util import time_uuid
from . import ActionNotRegistered, ActionAlreadyRegistered, Timeout
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
    def __init__(self, task_engine, task_id, job_id, action, args, kwargs):
        super(TaskRunner, self).__init__()
        self._engine = task_engine
        self._task_id = task_id
        self._job_id = job_id
        self._action = action
        self._args = args
        self._kwargs = kwargs

    @property
    def task_id(self):
        return self._task_id

    @property
    def job_id(self):
        return self._job_id

    def __repr__(self):
        return "Task[%s]" % self._task_id

    def _run(self):
        try:
            return self._action(*self._args, **self._kwargs)
        finally:
            self._engine.task_done(self)

    def stopped(self):
        """

        :return: True if the task has finished, either successfully or not.
        """
        return self.ready()

    def finished(self):
        """
        :return: True if the task has finished successfully.
        """
        return self.ready() and self.successful()

    def failed(self):
        return self.ready() and not self.successful()

    def result(self, timeout=None):
        try:
            res = self.get(block=True, timeout=timeout)
            if res is gevent.GreenletExit:
                raise res

            return res
        except gevent.Timeout:
            raise Timeout()
        except Exception:
            raise

    def __hash__(self):
        return hash(self._task_id)

    def __eq__(self, other):
        return self.task_id == other.task_id


class TaskEngine(object):

    def __init__(self):
        self.context = None
        self._actions = {}
        self._tasks = {}
        self._tasks_per_job = {}
        self._modules = {}

    def get_module_names(self):
        """

        :return: the list of names of registered action modules.
        """
        return self._modules.keys()

    def get_module_actions(self, mod_name):
        """

        :param mod_name: the module's name
        :return: the dict of actions in the specified module
        """
        return self._modules.get(mod_name)

    def start(self, ctx):
        _logger.debug("Starting task engine...")
        self.context = ctx
        self.context['taskengine'] = self

    def stop(self, ctx):
        _logger.debug("Stopping task engine...")

        gevent.killall(self._tasks.values())

    def register(self, func):
        action_key, mod_name, func_name = service.action_key(func.__module__, func.func_name)

        if self._actions.get(action_key) is not None:
            raise ActionAlreadyRegistered(action_key)

        _logger.debug("Action %s registered." % action_key)

        proxy = ActionProxy(self, func, action_key)
        self._actions[action_key] = proxy
        mod = self._modules.get(mod_name)
        if mod is None:
            mod = {}
            self._modules[mod_name] = mod

        mod[func_name] = proxy
        return proxy

    def unregister(self, task_key):
        proxy = self._actions.get(task_key)
        if proxy is not None:
            del self._actions[task_key]

        parts = task_key.split('.')
        mod = self._modules.get(parts[0])
        if mod:
            action = mod.get(parts[1])
            if action:
                del mod[parts[1]]

    def task_done(self, task):
        _logger.debug("Task '%s' is done for job '%s'", task.task_id, task.job_id)

        if task.task_id in self._tasks:
            del self._tasks[task.task_id]
        s = self._tasks_per_job.get(task.job_id)
        if s is not None:
            s.remove(task)

    def get_action(self, action_key):
        return self._actions.get(action_key)

    def do_task(self, job_id, action_key, *args, **kwargs):

        action = self._actions.get(action_key)
        if action is None:
            raise ActionNotRegistered(action_key)

        task_id = time_uuid.oid()
        task = TaskRunner(self, task_id, job_id, action, args, kwargs)
        self._tasks[task_id] = task

        s = self._tasks_per_job.get(job_id)
        if s is None:
            s = set()
            self._tasks_per_job[job_id] = s

        s.add(task)
        task.start()
        return task

    def release_for_job(self, job_id):
        """
        Release resources associated with the specified job.

        :param job_id: the job's ID.
        """

        _logger.debug("Releasing tasks for job: '%s'", job_id)
        s = self._tasks_per_job.get(job_id)
        if s is None:
            return

        gevent.killall(list(s))
