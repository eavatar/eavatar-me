# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Loading modules for exposing web resources or providing REST APIs.
"""
import os
import sys
import glob
import logging
from importlib import import_module

from ..runtime import environ
from .signals import MODULE_LOADED

logger = logging.getLogger(__name__)

_MODULES_DIR = os.path.join('mods')

# the package name for modules.
_MODULE_PKG = ''


class ModuleInfo(object):

    def __init__(self, name, mod):
        self._name = name
        self._mod = mod

    @property
    def name(self):
        return self._name

    @property
    def module(self):
        return self._mod

    @module.setter
    def module(self, mod):
        self._mod = mod


class ModuleEngine(object):
    """
    Responsible for managing application modules.
    """

    def __init__(self):
        self.modules = {}
        self.modules_path = os.path.join(environ.pod_dir(), _MODULES_DIR)
        self.modules_path = os.path.abspath(self.modules_path)

    def _scan_modules(self):
        pattern = os.path.join(self.modules_path, '[a-zA-Z][a-zA-Z0-9_]*.py')
        return glob.glob(pattern)

    def _load_modules(self, ctx):
        sys.path.append(self.modules_path)
        logger.debug("Module directory: %s", self.modules_path)

        module_files = self._scan_modules()

        logger.debug("Found %d module(s)" % len(module_files))

        for s in module_files:
            name = os.path.basename(s)
            if '__init__.py' == name:
                continue

            # gets the basename without extension part.
            name = os.path.splitext(name)[0]
            mod_name = _MODULE_PKG + name
            try:
                logger.debug("Loading module: %s", mod_name)
                mod = import_module(mod_name, _MODULE_PKG)
                mod_info = ModuleInfo(name, mod)
                self.modules[name] = mod_info

                ctx.send(signal=MODULE_LOADED, sender=self)
            except ImportError:
                logger.error("Failed to import module: %s", mod_name,
                             exc_info=True)

    def start(self, ctx):
        logger.debug("Starting module engine...")
        self._load_modules(ctx)
        logger.debug("Module engine started.")

    def stop(self, ctx):
        logger.debug("Module engine stopped.")