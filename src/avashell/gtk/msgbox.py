# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from gi.repository import Gtk
from avashell.base import Notice


def inform(title, message):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                               Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


def alert(title, message):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
                               Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


def error(title, message):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


def confirm(title, message):
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.QUESTION,
                               Gtk.ButtonsType.YES_NO, title)
    dialog.format_secondary_text(message)
    response = dialog.run()

    dialog.destroy()
    return response == Gtk.ResponseType.YES


def input(title, message):
    dialog = Gtk.MessageDialog(None,
                               Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               Gtk.MessageType.QUESTION,
                               Gtk.ButtonsType.OK_CANCEL,
                               title)
    dialog.format_secondary_text(message)

    dialogBox = dialog.get_content_area()
    userEntry = Gtk.Entry()
    # userEntry.set_visibility(True)
    # userEntry.set_invisible_char("*")
    userEntry.set_size_request(250, 0)
    userEntry.set_text("")
    dialogBox.pack_end(userEntry, False, False, 0)

    dialog.show_all()
    response = dialog.run()
    text = userEntry.get_text()
    dialog.destroy()
    if response == Gtk.ResponseType.OK:
        return text
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

    print(input("Input Text", "Please enter your name:"))

if __name__ == '__main__':
    _test()
