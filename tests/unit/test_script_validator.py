# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import ast
from ava.job.validator import ScriptValidator

import pytest


def test_import_not_allowed():
    script1 = """import os
    """

    validator = ScriptValidator()
    node = ast.parse(script1, filename='script1', mode='exec')
    with pytest.raises(Exception):
        validator.visit(node)

    script2 = """from os import path"""
    node = ast.parse(script2, filename='script2', mode='exec')
    with pytest.raises(Exception):
        validator.visit(node)


def test_func_definition_not_allowed():
    script = """def f():
        print('hi')
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    with pytest.raises(Exception):
        validator.visit(node)


def test_while_loop_not_allowed():
    script = """while True:
        print('hi')
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    with pytest.raises(Exception):
        validator.visit(node)


def test_exec_not_allowed():
    script = """
exec "print('hi')"
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    with pytest.raises(Exception):
        validator.visit(node)


def test_eval_not_allowed():
    script = """
eval('1+1')
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    with pytest.raises(Exception):
        validator.visit(node)


def test_name_with_double_underscores_not_allowed():
    script = """
__get('1+1')
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    with pytest.raises(Exception):
        validator.visit(node)


def test_func_call_is_allowed():
    script = """
a = b()
c = func2(1, 2, 3)
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    validator.visit(node)


def test_for_loop_is_allowed():
    script = """
for i in range(10):
    pass
    """

    node = ast.parse(script, filename='script1', mode='exec')
    validator = ScriptValidator()
    validator.visit(node)


