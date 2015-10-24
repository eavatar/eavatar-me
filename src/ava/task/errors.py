# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ..core import AvaError


class ActionAlreadyRegistered(AvaError):
    """ Raised to indicate a task is being registered with the same key as a
    existing one.
    """
    def __init__(self, action_key):
        super(ActionAlreadyRegistered, self).__init__()
        self.action_key = action_key

    def __str__(self):
        return "Task %s already registered." % self.action_key


class ActionNotRegistered(AvaError):
    """
    Raised when a task is not registered but is requested to schedule.
    """
    def __init__(self, action_key):
        super(ActionNotRegistered, self).__init__()
        self.action_key = action_key

    def __str__(self):
        return "Action %s not registered." % self.action_key


class Timeout(AvaError):
    """
    Raised to indicate a timeout occurred.
    """
    pass


__all__ = [
    'ActionAlreadyRegistered', 'ActionNotRegistered', 'Timeout',
]
