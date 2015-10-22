# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ..core import AvaError


class TaskAlreadyRegistered(AvaError):
    """ Raised to indicate a task is being registered with the same key as a
    existing one.
    """
    def __init__(self, task_key):
        super(TaskAlreadyRegistered, self).__init__()
        self.task_key = task_key

    def __str__(self):
        return "Task %s already registered." % self.task_key


class TaskNotRegistered(AvaError):
    """
    Raised when a task is not registered but is requested to schedule.
    """
    def __init__(self, task_key):
        super(TaskNotRegistered, self).__init__()
        self.task_key = task_key

    def __str__(self):
        return "Task %s not registered." % self.task_key

__all__ = [
    'TaskAlreadyRegistered', 'TaskNotRegistered',
]
