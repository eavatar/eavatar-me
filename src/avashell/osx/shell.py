# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals

import os
import click
import logging
import AppKit

from collections import Mapping

from Foundation import *  # noqa
from AppKit import *  # noqa

from avashell.utils import resource_path
from .. import base
from . import msgbox
from .cocoa import Delegate

_NOTIFICATIONS = True
try:
    from Foundation import NSUserNotification, NSUserNotificationCenter
except ImportError:
    _NOTIFICATIONS = False

logger = logging.getLogger(__name__)


def applicationSupportFolder(self):
    paths = NSSearchPathForDirectoriesInDomains(NSApplicationSupportDirectory,
                                                NSUserDomainMask, True)
    basePath = (len(paths) > 0 and paths[0]) or NSTemporaryDirectory()
    fullPath = basePath.stringByAppendingPathComponent_("Ava")
    if not os.path.exists(fullPath):
        os.mkdir(fullPath)
    return fullPath


def notification(title, subtitle, message, data=None, sound=True):
    """Send a notification to Notification Center (Mac OS X 10.8+).
    If running on a version of Mac OS X that does not support
    notifications, a ``RuntimeError`` will be raised. Apple says,

        "The userInfo content must be of reasonable serialized size
        (less than 1k) or an exception will be thrown."

    So don't do that!

    :param title: text in a larger font.
    :param subtitle: text in a smaller font below the `title`.
    :param message: text representing the body of the notification
                    below the `subtitle`.
    :param data: will be passed to the application's "notification
                 center" (see :func:`rumps.notifications`) when this
                 notification is clicked.
    :param sound: whether the notification should make a noise when
                  it arrives.
    """
    if not _NOTIFICATIONS:
        raise RuntimeError('Mac OS X 10.8+ is required to send notifications')
    if data is not None and not isinstance(data, Mapping):
        raise TypeError('notification data must be a mapping')
    _require_string_or_none(title, subtitle, message)
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(message)
    notification.setUserInfo_({} if data is None else data)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(
        NSDate.dateWithTimeInterval_sinceDate_(0, NSDate.date()))
    nc = NSUserNotificationCenter.defaultUserNotificationCenter()
    if nc is not None:
        nc.scheduleNotification_(notification)


def _require_string_or_none(*objs):
    for obj in objs:
        if not (obj is None or isinstance(obj, basestring)):
            raise TypeError(
                'a string or None is required but given {0}, a {1}'.format(
                    obj,
                    type(obj).__name__))


class AppDelegate(Delegate):
    status = 'Ready'

    def __init__(self):
        self.notices = []
        self.status_menu = None
        self._console = None

    def init(self):
        s = super(AppDelegate, self).init()
        if s is None:
            return None

        return s

    def applicationDidFinishLaunching_(self, sender):
        logger.debug("Application did finish launching.")

        logger.debug("Icon file: %s", resource_path('ava/res/eavatar.png'))
        statusbar = NSStatusBar.systemStatusBar()
        self.statusicon = statusbar.statusItemWithLength_(
            NSVariableStatusItemLength)
        self.icon = NSImage.alloc().initByReferencingFile_(
            resource_path('res/icon.png'))
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusicon.setImage_(self.icon)
        self.statusicon.setHighlightMode_(True)
        self.statusicon.setEnabled_(True)

        # make the menu
        self.menubarMenu = NSMenu.alloc().init()

        self.openItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            base.STR_OPEN_WEBFRONT, 'openWebfront:', '')
        self.menubarMenu.addItem_(self.openItem)

        self.openItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            base.STR_OPEN_FOLDER, 'openFolder:', '')
        self.menubarMenu.addItem_(self.openItem)

        self.menubarMenu.addItem_(base.NSMenuItem.separatorItem())

        mi = self.menubarMenu.addItemWithTitle_action_keyEquivalent_(
            base.STR_STATUS_MENU, None, "")
        self.create_status_menu()
        self.menubarMenu.setSubmenu_forItem_(self.status_menu, mi)

        self.menubarMenu.addItem_(NSMenuItem.separatorItem())

        mi = self.menubarMenu.addItemWithTitle_action_keyEquivalent_(
            base.STR_NOTICES_MENU, None, "")

        self.notices_menu = self.create_notices_menu()
        self.menubarMenu.setSubmenu_forItem_(self.notices_menu, mi)

        self.menubarMenu.addItem_(NSMenuItem.separatorItem())

        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            base.STR_EXIT, 'quitApp:', '')
        self.menubarMenu.addItem_(self.quit)

        # add menu to statusitem
        self.statusicon.setMenu_(self.menubarMenu)
        self.statusicon.setToolTip_(base.STR_STATUS)

    def applicationWillTerminate_(self, sender):
        logger.debug("Application will terminate.")

    def windowWillClose_(self, aNotification):
        logger.debug("Console window will close.")

    def windowShouldClose_(self, sender):
        logger.debug("Console window should close.")
        self.shell.console.hide()
        return False

    def userNotificationCenter_didActivateNotification_(self,
                                                        notification_center,
                                                        notification):
        notification_center.removeDeliveredNotification_(notification)
        data = dict(notification.userInfo())
        logger.debug("Notification: %s", data)

    def alert(self, msg, title="Important Message"):
        self.app.activateIgnoringOtherApps_(True)
        alert = NSAlert.alloc().init()
        alert.setMessageText_(title)
        alert.setInformativeText_(msg)
        alert.setAlertStyle_(NSInformationalAlertStyle)
        alert.runModal()

    def create_notices_menu(self):
        m = AppKit.NSMenu.alloc().initWithTitle_("Notices")
        return m

    def create_status_menu(self):
        self.status_menu = AppKit.NSMenu.alloc().initWithTitle_("Status")
        for i, s in enumerate(base.status.STRINGS):
            item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                s,
                'updateUserStatus:',
                '')
            if self.shell.user_status == i:
                item.setState_(1)
            self.status_menu.addItem_(item)

        return self.status_menu

    def clearNotices_(self, sender):
        logger.debug("Clear all messages.")
        self.notices_menu.removeAllItems()

    def showNotice_(self, sender):
        index = self.notices_menu.indexOfItem_(sender)
        logger.debug("Item index: %r" % index)

        notice = self.shell.get_notice_at(index)
        msgbox.show_notice(notice)

    def addNewNotice(self, notice, pop_last=False):
        mi = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            notice.title, 'showNotice:', '')
        self.notices_menu.insertItem_atIndex_(mi, 0)
        if pop_last:
            self.notices_menu.removeItemAtIndex_(NUM_OF_NOTICES)

    def status_(self, sender):
        pass

    def updateUserStatus_(self, sender):
        old_item = self.status_menu.itemAtIndex_(self.shell.user_status)
        old_item.setState_(0)
        index = self.status_menu.indexOfItem_(sender)
        self.shell.user_status = index
        sender.setState_(1)

    def openFolder_(self, sender):

        click.launch(launcher.get_app_dir())

    def openWebfront_(self, sender):
        self.shell.open_ui()

    def openConsole_(self, sender):
        if self.shell.console is None:
            self.shell.console = Console(self.shell)
        self.shell.console.show()

    def openHelp_(self, notification):

        self.shell.open_help()

    def quitApp_(self, notification):
        nsapplication = NSApplication.sharedApplication()
        logger.debug('closing application')
        nsapplication.terminate_(notification)


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()

        self.app = None
        self.delegate = None
        self.mainframe = None
        self.console = None

    def doIdle_(self, timer):
        self.process_idle_tasks()

    def on_user_notified(self, notice):
        try:
            pop_last = len(self.notices) >= base.NUM_OF_NOTICES
            print(len(self.notices))
            self.notices.append(notice)
            self.delegate.addNewNotice(notice, pop_last)

            if self.should_notify(notice):
                notification(title=notice.title, subtitle="",
                             message=notice.message)
        except:
            logger.error("Failed to send notice", exc_info=True)

    def _terminate(self):
        self.app.terminate_(None)

    def _run(self):
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(  # noqa
            1, self, 'doIdle:', "", True)
        self.app = NSApplication.sharedApplication()
        self.app.activateIgnoringOtherApps_(True)
        self.delegate = AppDelegate.alloc().init()
        self.delegate.shell = self
        self.delegate.app = self.app
        self.app.setDelegate_(self.delegate)

        if _NOTIFICATIONS:
            nc = NSUserNotificationCenter.defaultUserNotificationCenter()
            if nc is not None:
                nc.setDelegate_(self.app)
            else:
                logger.warning("No notification center object found!")
        else:
            logger.debug("Platform notification is not enabled.")

        self.app.run()
