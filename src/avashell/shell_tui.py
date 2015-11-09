# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ava import wrapper

wrapper.init_app_dir()


def main():
    from avashell.tui.shell import Shell
    shell = Shell()
    shell.run()

if __name__ == '__main__':
    main()
