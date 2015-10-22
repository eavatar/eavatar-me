# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import logging

from gi.repository import Gtk, Notify, GLib
from gi.repository import AppIndicator3 as appindicator

from avashell.utils import resource_path
from ava.user import status
from ..base import *
from . import msgbox

_logger = logging.getLogger(__name__)


class StatusIcon(object):
    def __init__(self, shell):
        self.shell = shell
        self.ind = appindicator.Indicator.new("EAvatar-indicator",
                                           resource_path("res/icon.png"),
                                           appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_icon_theme_path(resource_path('res/'))

        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon("icon.png")

        self.notices_menu = None
        self.status_menu = None
        self.old_status_item = None
        self.menu_setup()
        self.ind.set_menu(self.menu)
        self.notification = None
        Notify.init("EAvatar")

    def menu_setup(self):
        self.menu = Gtk.Menu()

        self.open_item = Gtk.MenuItem.new_with_label(STR_OPEN_FOLDER)
        self.open_item.connect("activate", self.on_open_folder)
        # self.open_item.show()
        self.open_webfront = Gtk.MenuItem.new_with_label(STR_OPEN_WEBFRONT)
        self.open_webfront.connect("activate", self.on_open_webfront)

        self.quit_item = Gtk.MenuItem.new_with_label(STR_EXIT)
        self.quit_item.connect("activate", self.quit)
        # self.quit_item.show()

        self.status_item = Gtk.MenuItem.new_with_label('Status')
        self.status_menu = self.create_status_menu()
        self.status_item.set_submenu(self.status_menu)
        self.notices_item = Gtk.MenuItem.new_with_label('Notices')

        self.notices_menu = Gtk.Menu()
        # self.notices_menu.append(Gtk.MenuItem.new_with_label('First notice'))
        self.notices_item.set_submenu(self.notices_menu)
        self.menu.append(self.open_webfront)
        self.menu.append(self.open_item)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.status_item)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.notices_item)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(self.quit_item)

        self.menu.show_all()

    def create_status_menu(self):
        menu = Gtk.Menu()
        for i, s in enumerate(status.STRINGS):
            item = Gtk.CheckMenuItem.new_with_label(s)
            item.status = i
            item.connect("activate", self.on_update_user_status)
            if self.shell.user_status == i:
                item.set_active(True)
                self.old_status_item = item
            menu.append(item)

        return menu

    def on_open_folder(self, sender):
        self.shell.open_folder()

    def on_open_webfront(self, sender):
        self.shell.open_ui()

    def on_open_help(self, sender):
        self.shell.open_help()

    def on_update_user_status(self, sender):
        if self.old_status_item is sender:
            return

        print("Status:", sender.status)

        self.old_status_item.set_active(False)
        self.shell.user_status = sender.status
        sender.set_active(True)
        self.old_status_item = sender

    def notify(self, msg, title="Ava Message"):
        if self.notification is None:
            self.notification = Notify.Notification.new(title, msg, resource_path("res/icon.png"))
            self.notification.set_app_name("EAvatar")
        else:
            self.notification.update(title, msg)
        self.notification.set_timeout(3)
        self.notification.show()

    def add_new_notice(self, notice, pop_last=False):
        item = Gtk.MenuItem.new_with_label(notice.title)
        item.connect("activate", self.on_show_notice)
        item.notice = notice
        item.show()

        self.notices_menu.prepend(item)

        if pop_last:
            self.notices_menu.remove(self.notices_menu.get_children()[-1])

    def on_show_notice(self, sender):
        _logger.debug("Show notice")
        msgbox.show_notice(sender.notice)

    def quit(self, widget):
        self.ind.set_status(appindicator.IndicatorStatus.PASSIVE)
        Gtk.main_quit()


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()
        self.statusIcon = StatusIcon(self)

    def notify_user(self, msg, title):
        _logger.debug("User notice received: %s", title)

        notice = Notice(title=title, message=msg)
        pop_last = len(self.notices) >= NUM_OF_NOTICES
        print(len(self.notices))
        self.notices.append(notice)
        self.statusIcon.add_new_notice(notice, pop_last)

        if self.should_notify(notice):
            self.statusIcon.notify(msg=msg, title=title)

    def on_timeout(self):
        self.process_idle_tasks()
        return True

    def _run(self):
        GLib.timeout_add(1000, self.on_timeout, priority=GLib.PRIORITY_DEFAULT)

        Gtk.main()


if __name__ == '__main__':
    shell = Shell()
    shell.run()

