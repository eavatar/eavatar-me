# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os
import logging
import shutil

from .. import APP_NAME
from ava.util import get_app_dir

POD_DIR_ENV = 'AVA_POD'

POD_DIR_NAME = u'pod'
PKGS_DIR_NAME = u'pkgs'
LOGS_DIR_NAME = u'logs'
DATA_DIR_NAME = u'data'
CONF_DIR_NAME = u'conf'
MODS_DIR_NAME = u'mods'

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


class Environment(object):
    """
    Encapsulates the runtime environment.
    """
    def __init__(self, app_name=APP_NAME):

        # Determines the location of the base directory which contains files
        # for a specific user.
        # This script assumes it is located at 'ava/runtime' sub-directory.
        from ..util import base_path

        self.base_dir = base_path()
        _logger.info("Work folder: %s" % self.base_dir)

        # Determines the location of the home directory.

        # self.pod_dir = os.path.join(self.base_dir, POD_DIR_NAME)
        self.pod_dir = get_app_dir(app_name)
        self.pod_dir = os.environ.get(POD_DIR_ENV, self.pod_dir)
        self.pod_dir = os.path.abspath(self.pod_dir)

        _logger.info("POD folder: %s" % self.pod_dir)

        self.conf_dir = os.path.join(self.pod_dir, CONF_DIR_NAME)
        self.pkgs_dir = os.path.join(self.pod_dir, PKGS_DIR_NAME)
        self.data_dir = os.path.join(self.pod_dir, DATA_DIR_NAME)
        self.logs_dir = os.path.join(self.pod_dir, LOGS_DIR_NAME)
        self.mods_dir = os.path.join(self.pod_dir, MODS_DIR_NAME)

        # Flag indicating if the runtime is launched by a shell.
        self.has_shell = False

    def init_pod_dir(self, folder):
        """
        Constructs the skeleton of directories if it not there already.
        :return:
        """
        _logger.debug("Initializing Pod folder...")
        if os.path.exists(folder):
            _logger.error("Pod folder '%s' exists, abort initialization." %
                          folder)
            return

        os.makedirs(folder)

        src_dir = os.path.join(self.base_dir, 'pod')
        # copy files from base_dir to user_dir
        subdirs = os.listdir(src_dir)
        # ignore_pattern = shutil.ignore_patterns("__init__.py")
        for d in subdirs:
            src_path = os.path.join(src_dir, d)
            dst_path = os.path.join(folder, d)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)


# The global environment.
_environ = None


def get_environ(app_name=APP_NAME, reset=False):
    global _environ

    if _environ and reset:
        _environ = None

    if _environ is None:
        _environ = Environment(app_name)

    return _environ


def base_dir():
    """
    Gets the base directory.
    :return:
    """
    return get_environ().base_dir


def pod_dir():
    """
    Gets the home directory.
    :return:
    """
    return get_environ().pod_dir


def conf_dir():
    """
    Gets the path for configuration files.

    :return: The configuration path.
    """
    return get_environ().conf_dir


def data_dir():
    """
    Gets the path for data files.

    :return: The path.
    """
    return get_environ().data_dir


def logs_dir():
    """
    Gets the path for log files.

    :return: The path.
    """
    return get_environ().logs_dir


def pkgs_dir():
    """
    Gets the path for packages files.

    :return: The path.
    """
    return get_environ().pkgs_dir


def mods_dir():
    return get_environ().mods_dir
