# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


import win32api
import win32con
import winerror
import win32gui_struct

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

import time
import struct
import commctrl

IDC_JOB_NAME = 1024
IDC_SCRIPT = 1025
IDC_BUTTON_CLOSE = 1030
IDC_BUTTON_SUBMIT = 1031
IDC_BUTTON_CLEAR = 1032


class NoticeDialog(object):
    """
    Modeless dialog for submitting a job.
    """
    def __init__(self, shell):
        win32gui.InitCommonControls()
        self.hinst = win32gui.dllhandle
        # win32api.LoadLibrary('MSFTEDIT.dll')
        self.shell = shell
        self.hicon = None
        self.list_data = {}
        self.className = "AvaNoticeDialog"
        self.title = 'Notice'
        self.hwnd = None
        self.job_name = 'job-1'
        self.script = ''

        self.hidden = False

    def _RegisterWndClass(self):
        message_map = {}
        wc = win32gui.WNDCLASS()
        wc.SetDialogProc()  # Make it a dialog class.
        wc.hInstance = self.hinst
        wc.lpszClassName = self.className
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW + 1
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        # C code: wc.cbWndExtra = DLGWINDOWEXTRA + sizeof(HBRUSH) + (sizeof(COLORREF));
        wc.cbWndExtra = win32con.DLGWINDOWEXTRA + struct.calcsize("Pi")
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE

        ## py.ico went away in python 2.5, load from executable instead
        this_app = win32api.GetModuleHandle(None)
        # wc.hIcon = self.hicon

        try:
            classAtom = win32gui.RegisterClass(wc)
        except win32gui.error, err_info:
            if err_info.winerror!=winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise
        return self.className

    def _GetDialogTemplate(self, dlgClassName):
        style = win32con.WS_POPUP | win32con.DS_MODALFRAME | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT | win32con.WS_MINIMIZEBOX
        cs = win32con.WS_CHILD | win32con.WS_VISIBLE

        # Window frame and title
        # font_name = 'COURIER'
        font_name = "MS Sans Serif"
        dlg = [ [self.title, (0, 0, 230, 180), style, None, (11, font_name), None, dlgClassName], ]

        # ID label and text box
        # dlg.append([130, 'Job Name:', -1, (5, 5, 220, 9), cs | win32con.SS_LEFT])
        # s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
        # dlg.append(['EDIT', None, IDC_JOB_NAME, (5, 15, 200, 12), s])

        dlg.append([130, 'Instructions:', -1, (5, 30, 220, 9), cs | win32con.SS_LEFT])
        s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER | win32con.ES_MULTILINE
        s |= win32con.WS_VSCROLL | win32con.ES_AUTOVSCROLL | win32con.ES_WANTRETURN
        dlg.append(['EDIT', None, IDC_SCRIPT, (5, 40, 220, 110), s])

        # OK/Cancel Buttons
        # (x positions don't matter here)
        s = cs | win32con.WS_TABSTOP
        # dlg.append([128, "Clear", IDC_BUTTON_CLEAR, (5, 155, 50, 14), s])
        dlg.append([128, "Close", IDC_BUTTON_CLOSE, (125, 155, 50, 14), s])
        s = win32con.BS_PUSHBUTTON | s
        dlg.append([128, "Submit", IDC_BUTTON_SUBMIT, (100, 155, 50, 14), s])

        return dlg

    def _DoCreate(self, fn):
        message_map = {
            win32con.WM_SIZE: self.OnSize,
            win32con.WM_COMMAND: self.OnCommand,
            win32con.WM_NOTIFY: self.OnNotify,
            win32con.WM_INITDIALOG: self.OnInitDialog,
            win32con.WM_CLOSE: self.OnClose,
            win32con.WM_DESTROY: self.OnDestroy,
        }

        dlgClassName = self._RegisterWndClass()
        template = self._GetDialogTemplate(dlgClassName)
        return fn(self.hinst, template, 0, message_map)

    def OnInitDialog(self, hwnd, msg, wparam, lparam):
        self.hwnd = hwnd
        # centre the dialog
        desktop = win32gui.GetDesktopWindow()
        l, t, r, b = win32gui.GetWindowRect(self.hwnd)
        dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(desktop)
        centre_x, centre_y = win32gui.ClientToScreen( desktop, ( (dt_r-dt_l)//2, (dt_b-dt_t)//2) )
        win32gui.MoveWindow(hwnd, centre_x-(r//2), centre_y-(b//2), r-l, b-t, 0)
        # self._SetupList()
        l, t, r, b = win32gui.GetClientRect(self.hwnd)
        self._DoSize(r-l, b-t, 1)

    def _DoSize(self, cx, cy, repaint=1):
        # right-justify the textbox.
        # ctrl = win32gui.GetDlgItem(self.hwnd, IDC_JOB_NAME)
        # win32gui.SetWindowText(ctrl, self.job_name)
        # l, t, r, b = win32gui.GetWindowRect(ctrl)
        # l, t = win32gui.ScreenToClient(self.hwnd, (l, t))
        # r, b = win32gui.ScreenToClient(self.hwnd, (r, b))
        # win32gui.MoveWindow(ctrl, l, t, cx-l-5, b-t, repaint)

        ctrl = win32gui.GetDlgItem(self.hwnd, IDC_SCRIPT)
        win32gui.SetFocus(ctrl)

        # The button.
        ctrl = win32gui.GetDlgItem(self.hwnd, IDC_BUTTON_SUBMIT)
        l, t, r, b = win32gui.GetWindowRect(ctrl)
        l, t = win32gui.ScreenToClient(self.hwnd, (l, t))
        r, b = win32gui.ScreenToClient(self.hwnd, (r, b))
        list_y = b + 10
        w = r - l
        win32gui.MoveWindow(ctrl, cx - 5 - w, t, w, b-t, repaint)

    def OnSize(self, hwnd, msg, wparam, lparam):
        x = win32api.LOWORD(lparam)
        y = win32api.HIWORD(lparam)
        self._DoSize(x, y)
        return 1

    def OnNotify(self, hwnd, msg, wparam, lparam):
        info = win32gui_struct.UnpackNMITEMACTIVATE(lparam)
        if info.code == commctrl.NM_DBLCLK:
            print("Double click on item", info.iItem+1)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == IDC_BUTTON_CLOSE:
            self.on_close_btn_clicked()
        elif id == IDC_BUTTON_SUBMIT:
            self.on_submit_btn_clicked()
        elif id == IDC_BUTTON_CLEAR:
            self.on_clear_btn_clicked()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        # print("OnDestroy")
        # win32gui.PostQuitMessage(0)
        win32gui.EndDialog(hwnd, 0)
        self.hwnd = None

    def CreateWindow(self):
        self._DoCreate(win32gui.DialogBoxIndirect)

    def run(self):
        while not win32gui.PumpWaitingMessages():
            self.shell.process_idle_tasks()
            time.sleep(0.1)

    def OnClose(self, hwnd, msg, wparam, lparam):
        print("OnClose")
        # win32gui.EndDialog(hwnd, 0)
        self.hide()
        # win32gui.PostQuitMessage(0)

    def show(self):
        # print("show")
        if self.hwnd:
            win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)
            self.hidden = False
            self._clear_script()

    def bring_to_top(self):
        if not self.hwnd:
            return

        # win32gui.BringWindowToTop(self.hwnd)
        win32gui.SetForegroundWindow(self.hwnd)

    def hide(self):
        print("hide")
        win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)
        self.hidden = True

    def on_submit_btn_clicked(self):
        print("Ok button pressed")
        # self.job_name = win32gui.GetDlgItemText(self.hwnd, IDC_JOB_NAME)
        self.script = win32gui.GetDlgItemText(self.hwnd, IDC_SCRIPT)
        print(self.job_name)
        job = dict(name=self.job_name, script=self.script)
        self.shell.submit_job(job)
        self._clear_script()

    def on_close_btn_clicked(self):
        self.hide()

    def on_clear_btn_clicked(self):
        self._clear_script()

    def _clear_script(self):
        ctrl = win32gui.GetDlgItem(self.hwnd, IDC_SCRIPT)
        win32gui.SetWindowText(ctrl, b'')
