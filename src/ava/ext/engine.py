# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from ..runtime.package import PackageManager
from .service import ExtensionManager

logger = logging.getLogger(__name__)


class ExtensionEngine(object):
    """
    Responsible for managing extension packages.
    """
    def __init__(self):
        self._extension_mgr = ExtensionManager()
        self._package_mgr = PackageManager()

    def start(self, ctx):
        logger.debug("Starting extension engine...")
        self._package_mgr.find_packages()
        self._extension_mgr.load_extensions()
        self._extension_mgr.start_extensions(ctx)
        logger.debug("Extension engine started.")

    def stop(self, ctx):
        logger.debug("Stopping extension engine...")
        self._extension_mgr.stop_extensions(ctx)
        logger.debug("Extension engine stopped.")
