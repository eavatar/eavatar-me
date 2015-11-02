# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import os
import time
import logging

import win32api
import win32con
import win32gui_struct
import timer

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

import itertools
import glob


from avashell.utils import resource_path
from ..base import *
from . import msgbox
from .console import Console

_logger = logging.getLogger(__name__)


class MainFrame(object):
    def __init__(self, message_map):
        self.window_class_name = "AvaWnd"
        self.hinst = None
        self.class_atom = self.register_wnd_class(message_map)
        self.hwnd = self.create_window()

    def register_wnd_class(self, message_map):
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        self.hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # could also specify a wndproc.
        return win32gui.RegisterClass(window_class)

    def create_window(self):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = win32gui.CreateWindow(self.class_atom,
                                     self.window_class_name,
                                     style,
                                     0,
                                     0,
                                     310,
                                     250,
                                     0,
                                     0,
                                     self.hinst,
                                     None)
        win32gui.UpdateWindow(hwnd)
        return hwnd

    def show(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)

    def close(self):
        win32gui.PostQuitMessage(0)


_QUIT = 'QUIT'

_FIRST_ID = 1023
_ID_OPEN_WEBFRONT = 1024
_ID_OPEN_FOLDER = 1026
_ID_OPEN_CONSOLE = 1027

_ID_NOTICE = 1030

_ID_STATUS_AVAILABLE = 1040
_ID_STATUS_BUSY = 1041
_ID_STATUS_AWAY = 1042
_ID_STATUS_DND = 1043

_ID_QUIT = 1100


class StatusIcon(object):
    def __init__(self, s):
        self.shell = s

        self.icons = itertools.cycle(glob.glob(resource_path('res/*.ico')))
        self.hover_text = STR_STATUS

        self.icon = self.icons.next()

        self.default_menu_index = 0

        self.notify_id = None
        self.hicon = None
        self.refresh_icon()
        self.notices_menu = win32gui.CreateMenu()
        self.status_menu = self._create_status_menu()
        self.notice_index = -1

    def refresh_icon(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            self.hicon = win32gui.LoadImage(hinst,
                                            self.icon,
                                            win32con.IMAGE_ICON,
                                            0,
                                            0,
                                            icon_flags)
        else:
            print("Can't find icon file - using default.")
            self.hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        self.notify_id = (self.shell.main_frame.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          self.hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.shell.main_frame.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.shell.main_frame.hwnd,
                                None)

    def update_status_menu(self, user_status):
        for i, s in enumerate(status.STRINGS):
            fstate = 0
            if user_status == i:
                fstate = win32con.MFS_CHECKED
            item, extras = win32gui_struct.PackMENUITEMINFO(
                text=status.STRINGS[i],
                hbmpItem=None,
                fState=fstate,
                wID=_ID_STATUS_AVAILABLE + i)
            win32gui.SetMenuItemInfo(self.status_menu, i, 1, item)

    def _create_status_menu(self):
        menu = win32gui.CreateMenu()
        for i, s in enumerate(status.STRINGS):
            fstate = 0
            if self.shell.user_status == i:
                fstate = win32con.MFS_CHECKED
            item, extras = win32gui_struct.PackMENUITEMINFO(
                text=status.STRINGS[i],
                hbmpItem=None,
                fState=fstate,
                wID=_ID_STATUS_AVAILABLE + i)
            win32gui.InsertMenuItem(menu, i, 1, item)

        self.status_menu = menu
        return self.status_menu

    def create_menu(self, menu):
        #        option_icon = self.prep_menu_icon(option_icon)
        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=STR_EXIT,
            hbmpItem=None,
            wID=_ID_QUIT)

        win32gui.InsertMenuItem(menu, 0, 1, item)

        win32gui.InsertMenu(menu, 0, win32con.MF_BYPOSITION,
                            win32con.MF_SEPARATOR, None)

        win32gui.InsertMenu(menu, 0, win32con.MF_POPUP | win32con.MF_BYPOSITION,
                            self.notices_menu, STR_NOTICES_MENU)


        win32gui.InsertMenu(menu, 0, win32con.MF_BYPOSITION,
                            win32con.MF_SEPARATOR, None)

        win32gui.InsertMenu(menu, 0, win32con.MF_POPUP | win32con.MF_BYPOSITION,
                            self.status_menu, STR_STATUS_MENU)

        win32gui.InsertMenu(menu, 0, win32con.MF_BYPOSITION,
                            win32con.MF_SEPARATOR, None)

        # item, extras = win32gui_struct.PackMENUITEMINFO(
        #     text=STR_OPEN_CONSOLE,
        #     hbmpItem=None,
        #     wID=_ID_OPEN_CONSOLE)
        # win32gui.InsertMenuItem(menu, 0, 1, item)

        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=STR_OPEN_FOLDER,
            hbmpItem=None,
            wID=_ID_OPEN_FOLDER)

        win32gui.InsertMenuItem(menu, 0, 1, item)

        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=STR_OPEN_WEBFRONT,
            hbmpItem=None,
            wID=_ID_OPEN_WEBFRONT)

        win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y,
                                   win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0,
                            win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def switch_icon(self):
        self.icon = self.icons.next()
        self.refresh_icon()

    def notify(self, message, title="Ava Message"):
        balloon_id = (self.shell.main_frame.hwnd,
                      0,
                      win32gui.NIF_INFO,
                      win32con.WM_USER + 20,
                      self.hicon,
                      self.hover_text,
                      title,
                      200,
                      message)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, balloon_id)

    def addNewNotice(self, notice, pop_last=False):
        self.notice_index = (self.notice_index + 1) % NUM_OF_NOTICES
        item, extras = win32gui_struct.PackMENUITEMINFO(
            text=notice.title,
            hbmpItem=None,
            wID=_ID_NOTICE + (self.notice_index % NUM_OF_NOTICES))

        win32gui.InsertMenuItem(self.notices_menu, 0, 1, item)
        if pop_last:
            win32gui.RemoveMenu(self.notices_menu, NUM_OF_NOTICES, win32con.MF_BYPOSITION)


class Shell(ShellBase):
    def __init__(self):
        super(Shell, self).__init__()

        msg_taskbar_restart = win32gui.RegisterWindowMessage("TaskbarCreated")
        self.message_map = {msg_taskbar_restart: self.OnRestart,
                            win32con.WM_DESTROY: self.OnDestroy,
                            win32con.WM_COMMAND: self.OnCommand,
                            win32con.WM_USER + 20: self.OnTaskbarNotify, }

        self.main_frame = MainFrame(self.message_map)
        self.status_icon = StatusIcon(self)
        self.notice_index = -1  # rolling index of topmost notice in the queue

        self.console = None
        self.destroyed = False

    def on_user_notified(self, notice):
        pop_last = len(self.notices) >= NUM_OF_NOTICES
        self.notice_index = (self.notice_index + 1) % NUM_OF_NOTICES
        self.notices.append(notice)

        self.status_icon.addNewNotice(notice, pop_last)

        if self.should_notify(notice):
            self.status_icon.notify(title=notice.title, message=notice.message)

    def job_accepted(self, job_name):
        if self.console is not None:
            self.console.append_message("Job accepted with name: %s" % job_name)
            self.console.clear_script()

    def job_rejected(self, reason):
        if self.console is not None:
            self.console.append_message("Job rejected with reason: %s" % reason)

    def job_failed(self, job_ctx):
        msg = "Job '%s' cannot be done: %r" % (job_ctx.name, job_ctx.exception.message)
        _logger.error(msg)
        if self.console is not None:
            self.console.append_message(msg)

    def job_finished(self, job_ctx):
        msg = "Job '%s' finished." % job_ctx.name
        _logger.info(msg)

        if self.console is None:
            return

        if job_ctx.result is not None:
            res = job_ctx.result
            if isinstance(res, tuple):
                res = repr(res)
            elif isinstance(res, unicode):
                res = repr(res)
            self.console.append_message(msg + '\r\n%s' % res)

        else:
            self.console.append_message(msg)

    def _timer_func(self, timer_id, tm):
        self.process_idle_tasks()

    def _run(self):
        timer.set_timer(100, self._timer_func)
        #while not win32gui.PumpWaitingMessages():
        #    self.process_idle_tasks()
        #    time.sleep(0.1)
        win32gui.PumpMessages()

    def _show_notice(self, item_id):
        _logger.debug("Show message")
        idx = (item_id - _ID_NOTICE)

        real_idx = (NUM_OF_NOTICES - idx + self.notice_index) % NUM_OF_NOTICES
        _logger.debug("Menu number: %d", real_idx)
        notice = self.notices[-(real_idx + 1)]

        if notice.kind == Notice.WARNING:
            msgbox.alert(title=notice.title, message=notice.message)
        elif notice.kind == Notice.ERROR:
            msgbox.error(title=notice.title, message=notice.message)
        else:
            msgbox.inform(title=notice.title, message=notice.message)

    def _show_console(self):
        if self.destroyed:
            return

        if self.console is None:
            self.console = Console(self)
            self.console.CreateWindow()
            _logger.debug("Console created.")

        _logger.debug("Show console")
        self.console.show()
        self.console.bring_to_top()

    def _update_user_status(self, item_id):
        old_status = self.user_status
        self.user_status = item_id - _ID_STATUS_AVAILABLE

        if old_status == self.user_status:
            return

        self.status_icon.update_status_menu(self.user_status)

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self.status_icon.refresh_icon()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.main_frame.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(_FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:
            self.status_icon.show_menu()
        # elif lparam == win32con.WM_LBUTTONUP:
        #    self._show_console()

        return True

    def execute_menu_option(self, id):
        if id == _ID_QUIT:
            win32gui.DestroyWindow(self.main_frame.hwnd)
        elif id == _ID_OPEN_FOLDER:
            self.open_folder()
        elif id == _ID_OPEN_WEBFRONT:
            self.open_ui()
        elif id == _ID_OPEN_CONSOLE:
            self._show_console()
        elif (_ID_NOTICE <= id < (_ID_NOTICE + NUM_OF_NOTICES)):
            self._show_notice(id)
        elif (_ID_STATUS_AVAILABLE <= id <= _ID_STATUS_DND):
            self._update_user_status(id)


if __name__ == '__main__':
    shell = Shell()
    shell.run()
