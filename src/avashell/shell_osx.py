# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
from ava import wrapper
from ctypes import cdll

wrapper.init_app_dir()
from ava.runtime import environ

from ava import exports

# nacl = cdll.LoadLibrary(os.path.join(environ.base_dir(), 'libsodium.dylib'))

# workaround for loading libsodium.dylib on Mac OSX
# os.chdir(environ.base_dir())

if __name__ == '__main__':

    from avashell.osx.shell import Shell
    shell = Shell()
    shell.run()
