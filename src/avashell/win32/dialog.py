# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .window import Window


class Dialog(Window):
    """
    Dialog
    """
    def __init__(self, dlg_template):
        super(Dialog, self).__init__()

    def on_init_dialog(self):
        pass

    def on_command(self):
        pass
