# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava.util import time_uuid


class Script(object):
    """
    Job scripts
    """
    def __init__(self, id=None, title='', text='', auto_start=False):
        if id is None:
            self._id = time_uuid.utcnow().hex
        else:
            self._id = id
        self._title = title
        self._text = text
        self._auto_start = auto_start

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text

    @property
    def auto_start(self):
        return self._auto_start

    def to_dict(self):
        return dict(
            id=self._id,
            title=self._title,
            text=self._text,
            auto_start=self._auto_start
        )

    def update(self, d):
        if d.get('title'):
            self._title = d.get('title')

        if d.get('text'):
            self._text = d.get('text')

        if d.get('auto_start'):
            self._auto_start = d.get('auto_start')
