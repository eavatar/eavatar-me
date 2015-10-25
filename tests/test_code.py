# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import code

script = """a='Hello There'
"""


def test_run_compiled_code():
    s = compile(script, '<string>', 'exec')
    exec s

