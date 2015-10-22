# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys

"""
For runtime compatibility.
"""

if sys.version_info < (2, 7):
    raise Exception('Ava requires Python 2.7 or higher.')


PY3 = sys.version_info[0] == 3
JYTHON = sys.platform.startswith('java')
PYPY = hasattr(sys, 'pypy_version_info')


if PY3:
    string_types = str,
    text_type = str
else:
    string_types = basestring,
    text_type = unicode