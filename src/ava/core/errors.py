# -*- coding: utf-8 -*-
"""
Base exceptions.
"""
from __future__ import absolute_import, division, print_function, unicode_literals


class AvaError(Exception):
    """
    Raised when error is framework-related but no specific error exists.
    """
    def __init__(self, *args, **kwargs):
        super(AvaError, self).__init__(args, kwargs)


class AgentStopped(AvaError):
    def __init__(self, *args, **kwargs):
        super(AgentStopped, self).__init__(args, kwargs)
