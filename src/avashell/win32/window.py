# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import win32con

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui


class Window(object):

    def __init__(self, message_map=None):
        if message_map:
            self.message_map = message_map
        else:
            self.message_map = self.default_message_map()

        self.window_class_name = b"EAvatarWnd"
        self.hinst = None
        self.class_atom = self._register_wnd_class(self.message_map)
        self.hwnd = self._create_window()

    def default_message_map(self):
        message_map = {
            win32con.WM_COMMAND: self._on_command,
            win32con.WM_DESTROY: self._on_destroy,
        }

        return message_map

    def _on_init_dialog(self, hwnd, msg, wparam, lparam):
        pass

    def _on_size(self, hwnd, msg, wparam, lparam):
        pass

    def _on_notify(self, hwnd, msg, wparam, lparam):
        pass

    def _on_command(self, hwnd, msg, wparam, lparam):
        pass

    def _on_destroy(self, hwnd, msg, wparam, lparam):
        win32gui.PostQuitMessage(0)

    def _on_close(self, hwnd, msg, wparam, lparam):
        win32gui.PostQuitMessage(0)

    def _register_wnd_class(self, message_map):
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        self.hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # could also specify a wndproc.
        return win32gui.RegisterClass(window_class)

    def _create_window(self,
                       style=win32con.WS_OVERLAPPED | win32con.WS_SYSMENU):
        # Create the Window.
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

    def hide(self):
        win32gui.HideWindow(self.hwnd)

    def close(self):
        win32gui.PostQuitMessage(0)


if __name__ == '__main__':
    win = Window()
    win.show()
    win32gui.PumpMessages()
