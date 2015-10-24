# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from . import bottle


logger = logging.getLogger(__name__)


class ApplicationDispatcher(object):
    """Allows one to mount middlewares or applications in a WSGI application.
    """

    def __init__(self, app, mounts=None):
        self.app = app
        self.mounts = mounts or {}

    def __call__(self, wsgi_env, start_response):
        script = wsgi_env.get(b'PATH_INFO', b'')
        # logger.debug("initial script: %s", script)
        path_info = b''
        while b'/' in script:
            if script in self.mounts:
                app = self.mounts[script]
                break
            script, last_item = script.rsplit(b'/', 1)
            # last_item = unicode(last_item, 'utf-8')
            path_info = b'/{0}{1}'.format(last_item, path_info)
        else:
            # logger.debug("Selected script: %s", script)
            app = self.mounts.get(script, self.app)
        original_script_name = wsgi_env.get(b'SCRIPT_NAME', b'')
        wsgi_env[b'SCRIPT_NAME'] = original_script_name + script
        wsgi_env[b'PATH_INFO'] = path_info
        return app(wsgi_env, start_response)

    def mount(self, path, app):
        # logger.debug("Mounting app at %s", path)
        if isinstance(path, unicode):
            path = path.encode('utf-8')
        self.mounts[path] = app
        return app

    def unmount(self, path):
        logger.debug("Unmounting app at %s", path)
        if isinstance(path, unicode):
            path = path.encode('utf-8')
        app = self.mounts.get(path)
        if app is not None:
            del self.mounts[path]
            return app
        return None

# the global web application
dispatcher = ApplicationDispatcher(bottle.app())

