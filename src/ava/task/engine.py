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


class TaskProxy(object):
    def __init__(self, task_engine, func):
        self.task_engine = task_engine
        self.func = func
        self.key = func.__module__ + '.' + func.func_name

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class TaskRunner(Greenlet):
    """ Represent running tasks, each of which is an invocation to a procedure.
    """
    def __init__(self, task_id, task, args, kwargs):
        super(TaskRunner, self).__init__(task, *args, **kwargs)
        self._task_id = task_id

    @property
    def task_id(self):
        return self._task_id

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


class Schedule(Greenlet):
    def __init__(self, sched_id, proc, args=None, kwargs=None):
        super(Schedule, self).__init__()
        self.id = sched_id
        self.proc = proc
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.error = None

    def call(self):
        try:
            _logger.debug("Before running task:")
            self.result = self.proc(*self.args, **self.kwargs)
            _logger.debug("Task result: %r", self.result)
            return self.result
        except Exception as ex:
            _logger.error("Error in calling task: %s", self.proc.key)
            self.error = ex

    @abstractmethod
    def _run(self):
        """
        Invoked to run
        """


class OnceSchedule(Schedule):
    def __init__(self, sched_id, proc, seconds=0, args=[], kwargs={}):
        super(OnceSchedule, self).__init__(sched_id, proc, args, kwargs)
        self.seconds = seconds

    def _run(self):
        if self.seconds > 0:
            gevent.sleep(self.seconds)
        self.call()


class PeriodicSchedule(Schedule):
    def __init__(self, sched_id, proc, interval, start_time=None,
                 stop_time=None, args=[], kwargs={}):
        super(PeriodicSchedule, self).__init__(sched_id, proc, args, kwargs)
        self.interval = interval
        self.start_time = start_time
        self.stop_time = stop_time
        self.next_run = 0

    def _run(self):
        now = datetime.now()
        if self.start_time is None:
            self.start_time = now

        if now < self.start_time:
            self.next_run = self.start_time - now
            gevent.sleep(self.next_run)

        while True:
            self.call()
            now = datetime.now()
            if self.stop_time and now >= self.stop_time:
                break
            self.next_run = self.interval
            gevent.sleep(self.next_run)


class TaskEngine(object):

    def __init__(self):
        self.context = None
        self._schedules = {}
        self._task_proxies = {}
        self._task_runners = {}

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
        task_key = service.action_key(func.__module__, func.func_name)
        if self._task_proxies.get(task_key) is not None:
            raise TaskAlreadyRegistered(task_key)

        proxy = TaskProxy(self, func)
        self._task_proxies[task_key] = proxy
        return proxy

    def unregister(self, task_key):
        proxy = self._task_proxies.get(task_key)
        if proxy is not None:
            del self._task_proxies[task_key]

    def get_task_proxy(self, task_key):
        return self._task_proxies.get(task_key)

    def do_task(self, action_key, *args, **kwargs):
        action = self._task_proxies[action_key]
        task_id = uuid1().hex
        runner = TaskRunner(task_id, action, *args, **kwargs)
        self._task_runners[task_id] = runner
        runner.start()
        return runner

    def run_once(self, task_key, delayed_secs, args, kwargs):
        """
        Schedules a one-time task.

        :param task_key:
        :param delayed_secs:
        :return: the schedule
        """

        task = self._task_proxies.get(task_key)
        if task is None:
            raise TaskNotRegistered(task_key)
        schedule_id = uuid1().hex
        schedule = OnceSchedule(schedule_id, task, delayed_secs, args, kwargs)
        self._schedules[schedule_id] = schedule
        schedule.start()
        return schedule

    def run_periodic(self, task_key, interval,
                     start_time=None, stop_time=None,
                     args=None, kwargs=None):
        """
        Schedules a periodic task.

        :param task_key:
        :param interval:
        :param start_time: If None, start immediately.
        :param stop_time: If None, the task run indefinitely.
        :return: the schedule
        """
        task = self._task_proxies.get(task_key)
        if task is None:
            raise TaskNotRegistered()

        schedule_id = uuid1().hex
        schedule = PeriodicSchedule(schedule_id, task, interval,
                                    start_time, stop_time,
                                    args, kwargs)
        self._schedules[schedule_id] = schedule
        schedule.start()
        return schedule

    def cancel(self, schedule):
        """
        Cancels the scheduled task.

        :param schedule_id:
        :return:
        """
        if schedule is None:
            return False
        del self._schedules[schedule.id]
        schedule.kill()
        return True

    def get_schedule(self, sched_id):
        """ Gets the schedule via the given id.

        :param sched_id: the schedule id.
        :return:
        """
        return self._schedules.get(sched_id)

