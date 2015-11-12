# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

DOIT_CONFIG = {'default_tasks': ['hello']}

sys.path.append(os.path.join('.', 'src'))


def is_windows():
    return sys.platform.startswith('win')


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


def task_make_dmg():
    settings_file = os.path.join('pack', 'dmg_settings.py')

    return {
        'actions': [['dmgbuild', '-s', settings_file, 'EAvatar ME', 'dist/avame.dmg']],
        'verbosity': 2
    }


def task_unit_test():
    test_path = os.path.join('tests', 'unit')
    cov_path = os.path.join('src', 'ava')

    return {
        'actions': [['py.test', '-s', '--cov', cov_path, '-vvv', test_path]],
        'verbosity': 2
    }


def task_int_test():
    test_path = os.path.join('tests', 'integration')
    cov_path = os.path.join('src', 'ava')

    return {
        'actions': [['py.test', '-s', '--cov-append', '--cov', cov_path, '-vvv', test_path]],
        'verbosity': 2
    }


def task_func_test():
    test_path = os.path.join('tests', 'functional')

    return {
        'actions': [['py.test', '-s', '-vvv', test_path]],
        'verbosity': 2
    }


def task_all_tests():
    unit_test_path = os.path.join('tests', 'unit')
    int_test_path = os.path.join('tests', 'integration')
    func_test_path = os.path.join('tests', 'functional')
    cov_path = os.path.join('src', 'ava')

    return {
        'actions': [
            ['flake8', 'src/ava'],
            ['py.test', '-s', '--cov', cov_path, '-vvv', unit_test_path],
            ['py.test', '-s', '--cov-append', '--cov', cov_path, '-vvv', int_test_path],
            ['py.test', '-s', '-vvv', func_test_path]
        ],
        'verbosity': 2
    }


def task_start_agent():
    script_path = os.path.join('src', 'avashell', 'shell_tui.py')

    if is_windows():
        os.environ['PYTHONPATH'] = '.;.\\src'
    else:
        os.environ['PYTHONPATH'] = '.:./src'

    return {
        'actions': [['python', script_path]],
        'verbosity': 2
    }


def task_flake8_check():
    return {
        'actions': [['flake8', 'src/ava']],
        'verbosity': 2
    }


def task_pylint_check():
    return {
        'actions': [['pylint', 'src/ava']],
        'verbosity': 2
    }
