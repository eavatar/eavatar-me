# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import pkg_resources

__all__ = ['Extension', 'ExtensionManager']

logger = logging.getLogger(__name__)


class Extension(object):
    def __init__(self, name, entry_point):
        self.name = name
        self.entry_point = entry_point
        self.cls = None
        self.obj = None

    def __repr__(self):
        return 'Extension(%s)' % self.name


class ExtensionManager(object):
    def __init__(self, namespace="ava.extension"):
        self.namespace = namespace
        self.extensions = []

    def load_extensions(self, invoke_on_load=True):
        for it in pkg_resources.working_set.iter_entry_points(self.namespace,
                                                              name=None):
            logger.debug("Loading extension: %s at module: %s", it.name,
                         it.module_name)
            logger.debug("")
            ext = Extension(it.name, it)
            ext.cls = it.load()

            if invoke_on_load:
                ext.obj = ext.cls()
            self.extensions.append(ext)

        # sort extensions by names
        self.extensions.sort(key=lambda e: e.name)
        logger.debug("Loaded extensions: %r", self.extensions)

    def start_extensions(self, context=None):
        for ext in self.extensions:
            startfun = getattr(ext.obj, "start", None)
            if startfun is not None and callable(startfun):
                    startfun(context)

    def stop_extensions(self, context=None):
        for ext in reversed(self.extensions):
            stopfun = getattr(ext.obj, "stop", None)
            if stopfun is not None and callable(stopfun):
                try:
                    stopfun(context)
                except Exception:
                    pass
