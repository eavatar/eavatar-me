# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import win32api
import win32con
import winerror
import win32gui_struct
import win32ui
from win32com.shell import shell, shellcon

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

import struct, array
import commctrl

IDC_SEARCHTEXT = 1024
IDC_BUTTON_CANCEL = 1025
IDC_BUTTON_OK = 1026

desktop_pidl = shell.SHGetFolderLocation (0, shellcon.CSIDL_DESKTOP, 0, 0)

WM_SEARCH_RESULT = win32con.WM_USER + 512
WM_SEARCH_FINISHED = win32con.WM_USER + 513


class _WIN32MASKEDSTRUCT:

    def __init__(self, **kw):
        full_fmt = ""
        for name, fmt, default, mask in self._struct_items_:
            self.__dict__[name] = None
            if fmt == "z":
                full_fmt += "pi"
            else:
                full_fmt += fmt
        for name, val in kw.iteritems():
            if name not in self.__dict__:
                raise ValueError("LVITEM structures do not have an item '%s'" % (name,))
            self.__dict__[name] = val

    def __setattr__(self, attr, val):
        if not attr.startswith("_") and attr not in self.__dict__:
            raise AttributeError(attr)
        self.__dict__[attr] = val

    def toparam(self):
        self._buffs = []
        full_fmt = ""
        vals = []
        mask = 0
        # calc the mask
        for name, fmt, default, this_mask in self._struct_items_:
            if this_mask is not None and self.__dict__.get(name) is not None:
                mask |= this_mask
        self.mask = mask
        for name, fmt, default, this_mask in self._struct_items_:
            val = self.__dict__[name]
            if fmt == "z":
                fmt = "Pi"
                if val is None:
                    vals.append(0)
                    vals.append(0)
                else:
                    # Note this demo still works with byte strings.  An
                    # alternate strategy would be to use unicode natively
                    # and use the 'W' version of the messages - eg,
                    # LVM_SETITEMW etc.
                    val = val + "\0"
                    if isinstance(val, unicode):
                        val = val.encode("mbcs")
                    str_buf = array.array("b", val)
                    vals.append(str_buf.buffer_info()[0])
                    vals.append(len(val))
                    self._buffs.append(str_buf) # keep alive during the call.
            else:
                if val is None:
                    val = default
                vals.append(val)
            full_fmt += fmt
        return struct.pack(*(full_fmt,) + tuple(vals))


# NOTE: See the win32gui_struct module for an alternative way of dealing
# with these structures
class LVITEM(_WIN32MASKEDSTRUCT):
    _struct_items_ = [
        ("mask", "I", 0, None),
        ("iItem", "i", 0, None),
        ("iSubItem", "i", 0, None),
        ("state", "I", 0, commctrl.LVIF_STATE),
        ("stateMask", "I", 0, None),
        ("text", "z", None, commctrl.LVIF_TEXT),
        ("iImage", "i", 0, commctrl.LVIF_IMAGE),
        ("lParam", "i", 0, commctrl.LVIF_PARAM),
        ("iIdent", "i", 0, None),
    ]


class LVCOLUMN(_WIN32MASKEDSTRUCT):
    _struct_items_ = [
        ("mask", "I", 0, None),
        ("fmt", "i", 0, commctrl.LVCF_FMT),
        ("cx", "i", 0, commctrl.LVCF_WIDTH),
        ("text", "z", None, commctrl.LVCF_TEXT),
        ("iSubItem", "i", 0, commctrl.LVCF_SUBITEM),
        ("iImage", "i", 0, commctrl.LVCF_IMAGE),
        ("iOrder", "i", 0, commctrl.LVCF_ORDER),
    ]


def MakeLoginDlgTemplate(title):
    style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE

    # Window frame and title
    dlg = [[title, (0, 0, 184, 40), style, None, (8, "MS Sans Serif")], ]

    # ID label and text box
    dlg.append([130, "User ID:", -1, (7, 9, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['EDIT', None, win32ui.IDC_EDIT1, (50, 7, 60, 12), s])

    # Password label and text box
    dlg.append([130, "Password:", -1, (7, 22, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['EDIT', None, win32ui.IDC_EDIT2, (50, 20, 60, 12),
                s | win32con.ES_PASSWORD])

    # OK/Cancel Buttons
    s = cs | win32con.WS_TABSTOP
    dlg.append([128, "OK", win32con.IDOK, (124, 5, 50, 14),
                s | win32con.BS_DEFPUSHBUTTON])
    s = win32con.BS_PUSHBUTTON | s
    dlg.append([128, "Cancel", win32con.IDCANCEL, (124, 20, 50, 14), s])
    return dlg


def MakePasswordDlgTemplate(title):
    style = win32con.DS_MODALFRAME | win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT
    cs = win32con.WS_CHILD | win32con.WS_VISIBLE
    # Window frame and title
    dlg = [[title, (0, 0, 177, 45), style, None, (8, "MS Sans Serif")], ]

    # Password label and text box
    dlg.append([130, "Password:", -1, (7, 7, 69, 9), cs | win32con.SS_LEFT])
    s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
    dlg.append(['EDIT', None, win32ui.IDC_EDIT1, (50, 7, 60, 12),
                s | win32con.ES_PASSWORD])

    # OK/Cancel Buttons
    s = cs | win32con.WS_TABSTOP | win32con.BS_PUSHBUTTON
    dlg.append([128, "OK", win32con.IDOK, (124, 5, 50, 14),
                s | win32con.BS_DEFPUSHBUTTON])
    dlg.append([128, "Cancel", win32con.IDCANCEL, (124, 22, 50, 14), s])
    return dlg


class InputDialog(object):
    def __init__(self, title='Input Dialog', message='Enter text:'):
        win32gui.InitCommonControls()
        self.hinst = win32gui.dllhandle
        self.list_data = {}
        self.className = "AvaInputDialog"
        self.title = title
        self.message = message
        self.hwnd = None
        self.value = None

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
        try:
            wc.hIcon = win32gui.LoadIcon(this_app, 1)    ## python.exe and pythonw.exe
        except win32gui.error:
            wc.hIcon=win32gui.LoadIcon(this_app, 135)  ## pythonwin's icon
        try:
            classAtom = win32gui.RegisterClass(wc)
        except win32gui.error, err_info:
            if err_info.winerror!=winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise
        return self.className

    def _GetDialogTemplate(self, dlgClassName):
        style =  win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.DS_SETFONT | win32con.WS_MINIMIZEBOX
        cs = win32con.WS_CHILD | win32con.WS_VISIBLE

        # Window frame and title
        dlg = [ [self.title, (0, 0, 210, 60), style, None, (8, "MS Sans Serif"), None, dlgClassName], ]

        # ID label and text box
        dlg.append([130, self.message, -1, (5, 5, 200, 9), cs | win32con.SS_LEFT])
        s = cs | win32con.WS_TABSTOP | win32con.WS_BORDER
        dlg.append(['EDIT', None, IDC_SEARCHTEXT, (5, 15, 200, 12), s])

        # Search/Display Buttons
        # (x positions don't matter here)
        s = cs | win32con.WS_TABSTOP
        dlg.append([128, "Cancel", IDC_BUTTON_CANCEL, (100, 35, 50, 14), s])
        s = win32con.BS_PUSHBUTTON | s
        dlg.append([128, "OK", IDC_BUTTON_OK, (100, 35, 50, 14), s | win32con.BS_DEFPUSHBUTTON])

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
        l,t,r,b = win32gui.GetWindowRect(self.hwnd)
        dt_l, dt_t, dt_r, dt_b = win32gui.GetWindowRect(desktop)
        centre_x, centre_y = win32gui.ClientToScreen( desktop, ( (dt_r-dt_l)//2, (dt_b-dt_t)//2) )
        win32gui.MoveWindow(hwnd, centre_x-(r//2), centre_y-(b//2), r-l, b-t, 0)
        # self._SetupList()
        l,t,r,b = win32gui.GetClientRect(self.hwnd)
        self._DoSize(r-l, b-t, 1)

    def _DoSize(self, cx, cy, repaint = 1):
        # right-justify the textbox.
        ctrl = win32gui.GetDlgItem(self.hwnd, IDC_SEARCHTEXT)
        l, t, r, b = win32gui.GetWindowRect(ctrl)
        l, t = win32gui.ScreenToClient(self.hwnd, (l,t) )
        r, b = win32gui.ScreenToClient(self.hwnd, (r,b) )
        win32gui.MoveWindow(ctrl, l, t, cx-l-5, b-t, repaint)
        # The button.
        ctrl = win32gui.GetDlgItem(self.hwnd, IDC_BUTTON_OK)
        l, t, r, b = win32gui.GetWindowRect(ctrl)
        l, t = win32gui.ScreenToClient(self.hwnd, (l,t) )
        r, b = win32gui.ScreenToClient(self.hwnd, (r,b) )
        list_y = b + 10
        w = r - l
        win32gui.MoveWindow(ctrl, cx - 5 - w, t, w, b-t, repaint)

    def OnSize(self, hwnd, msg, wparam, lparam):
        x = win32api.LOWORD(lparam)
        y = win32api.HIWORD(lparam)
        self._DoSize(x,y)
        return 1

    def OnNotify(self, hwnd, msg, wparam, lparam):
        info = win32gui_struct.UnpackNMITEMACTIVATE(lparam)
        if info.code == commctrl.NM_DBLCLK:
            print("Double click on item", info.iItem+1)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == IDC_BUTTON_CANCEL:
            print("Cancel button pressed.")
            win32gui.EndDialog(hwnd, 0)
        elif id == IDC_BUTTON_OK:
            print("Ok button pressed")
            self.value = win32gui.GetDlgItemText(self.hwnd, IDC_SEARCHTEXT)
            print(self.value)
            win32gui.EndDialog(hwnd, 1)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        pass

    def DoModal(self):
        if self._DoCreate(win32gui.DialogBoxIndirect):
            return self.value
        else:
            return None

    def OnClose(self, hwnd, msg, wparam, lparam):
        win32gui.EndDialog(hwnd, 0)


def getTextInput(title='Input Dialog', message='Enter text:'):
    w=InputDialog(title, message)
    return w.DoModal()


def chooseOpenFolder():
    """
    Open a dialog for user to choose a folder/directory.

    :return: the path to the folder, or None if not selected.
    """

    pidl, display_name, image_list = shell.SHBrowseForFolder (
        win32gui.GetDesktopWindow (),
        desktop_pidl,
        "Choose a folder",
        0,
        None,
        None
    )

    if pidl is None:
        return None

    return shell.SHGetPathFromIDList(pidl)


# Test code
if __name__ == '__main__':
    # print(chooseOpenFolder())
    print(getTextInput())
