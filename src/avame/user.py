# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ava.core import get_core_context
from ava.task import action
from ava.user.signals import USER_NOTIFIED
from ava.user.models import Notice


@action
def notify(**kwargs):
    """
    Send a user notification.

    :param message: the message
    :param title: the title
    """
    notice = Notice(**kwargs)
    get_core_context().send(signal=USER_NOTIFIED, notice=notice)


__all__ = ['notify']
