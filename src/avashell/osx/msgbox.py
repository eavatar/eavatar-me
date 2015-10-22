# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from AppKit import *

from avashell.base import Notice


def inform(title, message):
    alert = NSAlert.alloc().init()
    alert.setMessageText_(title)
    alert.setInformativeText_(message)
    alert.setAlertStyle_(NSInformationalAlertStyle)
    alert.runModal()


def alert(title, message):
    alert = NSAlert.alloc().init()
    # alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSWarningAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.runModal()


def error(title, message):
    alert = NSAlert.alloc().init()
    # alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSCriticalAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.runModal()


def confirm(title, message):
    alert = NSAlert.alloc().init()
    # alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSWarningAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    alert.addButtonWithTitle_('OK')
    alert.addButtonWithTitle_('Cancel')

    result = alert.runModal()
    return result == NSAlertFirstButtonReturn


def input(title, message):
    alert = NSAlert.alloc().init()
    # alert.icon = Icon.app_icon._impl
    alert.setAlertStyle_(NSWarningAlertStyle)
    alert.setMessageText_(title)
    alert.setInformativeText_(message)

    text = NSTextField.alloc().initWithFrame_(NSMakeRect(0, 0, 240, 24))
    alert.setAccessoryView_(text)
    alert.addButtonWithTitle_('OK')
    alert.addButtonWithTitle_('Cancel')

    result = alert.runModal()
    if result == NSAlertFirstButtonReturn:
        return text.stringValue()
    else:
        return None


def show_notice(notice):
    if notice.kind == Notice.WARNING:
        alert(title=notice.title, message=notice.message)
    elif notice.kind == Notice.ERROR:
        error(title=notice.title, message=notice.message)
    else:
        inform(title=notice.title, message=notice.message)


def _test():
    inform(message="Sample message", title='msgbox.inform')
    alert(message="Alert message", title='msgbox.alert')
    error(message="Error message", title='msgbox.error')

    p = confirm(message="You are trying to do something dangerous", title="Are you sure?")
    if p:
        inform("Your answer", "You agreed.")
    else:
        inform("Your answer", "You disagreed.")

    text = input("Your name please", "Input your name")
    if text:
        inform(message=text, title="Your input")


if __name__ == '__main__':
    _test()


