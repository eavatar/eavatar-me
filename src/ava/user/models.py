# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class Notice(object):
    """
    Represent user notices.
    """
    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, title, message, kind=INFO):
        self._title = title
        self._message = message
        self._kind = kind
        self._uuid = None
        self._priority = None
        self._app_icon = None
        self._app_name = None
        self._reply_to = None

    @property
    def title(self):
        return self._title

    @property
    def message(self):
        return self._message

    @property
    def kind(self):
        return self._kind


