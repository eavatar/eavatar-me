# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import win32api
import win32con

from avashell.base import Notice


def inform(title, message, wnd=None):
    """ Display information to user.

    :param title:
    :param message:
    """
    win32api.MessageBox(wnd, message, title,
                        win32con.MB_OK | win32con.MB_ICONINFORMATION)


def confirm(title, message, wnd=None):
    """ Confirm with the user.

    :param title: The message title
    :param message: the message body
    :return: True if user agreed; False, otherwise.
    """
    answer = win32api.MessageBox(wnd, message, title,
                                 win32con.MB_YESNO | win32con.MB_ICONQUESTION)
    return answer == win32con.IDYES


def alert(title, message, wnd=None):
    """ Make a warning.

    :param title:
    :param message:
    """
    win32api.MessageBox(wnd, message, title,
                        win32con.MB_OK | win32con.MB_ICONWARNING)


def error(title, message, wnd=None):
    """ Show error message.

    :param title:
    :param message:
    """
    win32api.MessageBox(wnd, message, title,
                        win32con.MB_OK | win32con.MB_ICONERROR)


def show_notice(notice):
    if notice.kind == Notice.WARNING:
        alert(title=notice.title, message=notice.message)
    elif notice.kind == Notice.ERROR:
        error(title=notice.title, message=notice.message)
    else:
        inform(title=notice.title, message=notice.message)


if __name__ == '__main__':
    inform(message="Sample message", title='msgbox.inform')
    alert(message="Alert message", title='msgbox.alert')
    error(message="Error message", title='msgbox.error')

    p = confirm(message="You are trying to do something dangerous",
                title="Are you sure?")
    if p:
        inform("Your answer", "You agreed.")
    else:
        inform("Your answer", "You disagreed.")
