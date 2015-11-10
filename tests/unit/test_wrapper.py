# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import pytest

from ava.wrapper import init_app_dir

@pytest.fixture
def app_folder(tmpdir):
    dir = tmpdir.mkdir("data")
    return dir.dirname


def test_should_create_app_user_dir_correctly(app_folder):

    assert os.path.exists(app_folder)
    assert os.path.isdir(app_folder)

    target_folder = os.path.join(app_folder, 'pod')

    init_app_dir(target_folder)

    subdirs = list()
    subdirs.append('conf')
    subdirs.append('data')
    subdirs.append('jobs')
    subdirs.append('logs')
    subdirs.append('mods')
    subdirs.append('pkgs')
    subdirs.append('scripts')

    for subdir in subdirs:
        dst_dir = os.path.join(target_folder, subdir)
        print(dst_dir)
        assert os.path.exists(dst_dir)
        assert os.path.isdir(dst_dir)
