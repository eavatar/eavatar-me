# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
import logging
import shutil
import multiprocessing
from logging import NullHandler

from ava.core.agent import start_agent
from ava.util import base_path, get_app_dir
from ava.util.defines import POD_FOLDER_NAME

# makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()

_logger = logging.getLogger(__name__)
_logger.addHandler(NullHandler())


def init_app_dir(folder=None):
    """
    Constructs the skeleton of directories if it not there already.
    :return:
    """
    if folder is None:
        folder = get_app_dir()

    print("Initializing app user folder: %s" % folder)
    if os.path.exists(folder):
        _logger.warning("App user folder '%s' exists, abort initialization." %
                        folder)
        return

    os.makedirs(folder)

    src_dir = os.path.join(base_path(), POD_FOLDER_NAME)

    # copy files from base_dir to user_dir
    subdirs = os.listdir(src_dir)
    # ignore_pattern = shutil.ignore_patterns("__init__.py")

    subdirs.append('logs')
    subdirs.append('data')
    subdirs.append('mods')
    subdirs.append('jobs')
    subdirs.append('pkgs')
    subdirs.append('scripts')

    for d in subdirs:
        src_path = os.path.join(src_dir, d)
        dst_path = os.path.join(folder, d)
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.copytree(src_path, dst_path)
        elif os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)

    for d in subdirs:
        dst_path = os.path.join(folder, d)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)


def launch(inbox, outbox):
    app_dir = get_app_dir()
    _logger.info("App dir: %s" % app_dir)

    if not os.path.exists(app_dir):
        init_app_dir(app_dir)

    if not os.path.isdir(app_dir):
        _logger.error("Invalid app folder: %s" % app_dir)
        sys.exit(-1)

    start_agent(inbox, outbox)
