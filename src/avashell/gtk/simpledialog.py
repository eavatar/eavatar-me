# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from gi.repository import Gtk


def chooseOpenFolder():
    dialog = Gtk.FileChooserDialog("Please choose a folder", None,
                                   Gtk.FileChooserAction.SELECT_FOLDER,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    "Select", Gtk.ResponseType.OK))
    dialog.set_default_size(800, 400)

    response = dialog.run()
    filename = dialog.get_filename()
    dialog.destroy()

    if response == Gtk.ResponseType.OK:
        return filename

    return None


def chooseOpenFile():
    dialog = Gtk.FileChooserDialog("Please choose a file", None,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    # self.add_filters(dialog)

    response = dialog.run()
    filename = dialog.get_filename()

    dialog.destroy()

    if response == Gtk.ResponseType.OK:
        return filename


def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

if __name__ == '__main__':
    print(chooseOpenFile())
    print(chooseOpenFolder())
