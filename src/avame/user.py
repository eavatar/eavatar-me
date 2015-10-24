# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava.core import get_core_context
from ava.task import action
from ava.user.signals import USER_NOTIFIED


@action
def notify(msg, title):
    """
    Send a user notification.

    :param message: the message
    :param title: the title
    """
    get_core_context().send(signal=USER_NOTIFIED, msg=msg, title=title)


__all__ = ['notify']
