# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava.core import AvaError


class JobCancelledError(AvaError):
    pass


class ScriptSyntaxError(AvaError):
    def __init__(self, *args, **kwargs):
        super(ScriptSyntaxError, self).__init__(*args, **kwargs)
