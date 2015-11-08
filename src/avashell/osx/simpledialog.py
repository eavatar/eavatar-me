# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from AppKit import *  # noqa


def chooseOpenFolder():
    panel = NSOpenPanel.openPanel()
    panel.setCanCreateDirectories_(True)
    panel.setCanChooseDirectories_(True)
    panel.setCanChooseFiles_(False)
    panel.setResolvesAliases_(True)
    panel.setAllowsMultipleSelection_(False)
    result = panel.runModalForDirectory_file_types_(None, None, None)
    if result == NSOKButton:
        return panel.filename()
    return None


def chooseOpenFile():
    """
    :return: the
    """
    panel = NSOpenPanel.openPanel()
    panel.setCanCreateDirectories_(True)
    panel.setCanChooseDirectories_(False)
    panel.setCanChooseFiles_(True)
    panel.setAllowsMultipleSelection_(False)
    if panel.runModal() == NSOKButton:
        return panel.filename()
    return None


if __name__ == '__main__':
    # print(chooseOpenFile())
    print(chooseOpenFolder())
