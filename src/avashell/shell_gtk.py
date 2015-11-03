# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava import wrapper

wrapper.init_app_dir()
from ava.runtime import environ

from ava import exports


if __name__ == '__main__':

    from avashell.gtk.shell import Shell
    shell = Shell()
    shell.run()
