# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime
from ava.util import time_uuid
from ava import APP_NAME


class Notice(object):
    """
    Represent user notices.
    """
    INFO = 20
    WARNING = 30
    ERROR = 40

    NOTIFY = 1      # notification.
    CONFIRM = 2     # yes or no question.
    ASK_TEXT = 3    # ask for a text input from the user.
    ASK_SECRET = 4  # ask for a secret, like password, from the user

    def __init__(self, **kwargs):
        self._id = kwargs.get('id', time_uuid.oid())
        self._title = kwargs.get('title', '')
        self._message = kwargs.get('message', '')
        self._kind = kwargs.get('kind', self.NOTIFY)
        self._timestamp = kwargs.get('timestamp', datetime.now().isoformat())
        self._priority = kwargs.get('priority', self.INFO)
        self._app_icon = None
        self._app_name = APP_NAME
        self._reply_to = None

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def message(self):
        return self._message

    @property
    def kind(self):
        return self._kind

    @property
    def priority(self):
        return self._priority

    def to_dict(self):
        return dict(
            id=self._id,
            message=self._message,
            title=self._title,
            priority=self._priority,
            timestamp=self._timestamp,
            kind=self._kind
        )

    def from_dict(self, d):
        self._id = d.get('id')
        self._message = d.get('message')
        self._title = d.get('title')
        self._priority = d.get('priority')
        self._kind = d.get('kind')
        self._timestamp = d.get('timestamp')


