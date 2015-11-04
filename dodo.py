# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

DOIT_CONFIG = {'default_tasks': ['hello']}


def task_hello():
    """hello"""
    def python_hello(targets):
        print("Hi")

    return {
        'actions': [python_hello]
    }


def task_pack_gui():

    spec_file = os.path.join('pack', 'avame.spec')

    return {
        'actions': [['pyinstaller', spec_file, '--clean', '-y']],
    }


def task_pack_tui():

    spec_file = os.path.join('pack', 'avame-tui.spec')

    return {
        'actions': [['pyinstaller', spec_file, '--clean', '-y']],
    }


def task_unit_test():
    test_path = os.path.join('tests', 'unit')
    conv_path = os.path.join('src', 'ava')

    return {
        'actions': [['py.test', '-s', '-vvv', test_path]],
        'verbosity': 2
    }


def task_int_test():
    test_path = os.path.join('tests', 'integration')

    return {
        'actions': [['py.test', '-s', '-vvv', test_path]],
        'verbosity': 2
    }


def task_functional_test():
    test_path = os.path.join('tests', 'functional')

    return {
        'actions': [['py.test', '-s', '-vvv', test_path]],
        'verbosity': 2
    }

