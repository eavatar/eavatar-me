# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os
import logging

import gevent
from gevent.pywsgi import WSGIServer
from ava.runtime import settings
from ava.runtime import environ

from . import bottle

from . import resources

logger = logging.getLogger(__name__)

_CONF_SECTION = 'WEBFRONT'


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


class WebfrontEngine(object):
    """
    The client-facing web interface.
    """
    def __init__(self):
        logger.debug("Initializing webfront engine...")
        self._http_listener = None
        self._https_listener = None
        self.listen_port = 5000
        self.listen_addr = '127.0.0.1'
        self.secure_listen_port = 0  # 0 means not binding
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

    def start(self, ctx=None):
        logger.debug("Starting webfront engine...")

        if not settings[_CONF_SECTION]['enabled']:
            logger.debug("Webfront is not enabled.")
            return

        self.listen_port = settings[_CONF_SECTION]['listen_port']
        self.listen_addr = settings[_CONF_SECTION]['listen_addr']
        self.secure_listen_port = settings[_CONF_SECTION]['secure_listen_port']
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

        logger.debug("Local base URL:%s", self.local_base_url)

        if self.listen_port > 0:
            ctx.add_child_greenlet(gevent.spawn(self._run_http))

        if self.secure_listen_port > 0:
            ctx.add_child_greenlet(gevent.spawn(self._run_https))
        else:
            logger.debug("HTTPS listener is disabled.")

        ctx.bind('webfront', self)
        logger.debug("Webfront engine started.")

    def stop(self, ctx=None):
        logger.debug("Webfront engine stopped.")

    def _run_https(self):
        logger.debug("Webfront engine(HTTPS) is running...")

        conf_dir = environ.conf_dir()
        keyfile = os.path.join(conf_dir, 'ava.key')
        certfile = os.path.join(conf_dir, 'ava.crt')

        self._https_listener = WSGIServer(
            (self.listen_addr, self.secure_listen_port),
            dispatcher,
            keyfile=keyfile,
            certfile=certfile)

        logger.debug("Webfront engine(HTTPS) is listening on port: %d",
                     self._https_listener.address[1])

        self._https_listener.serve_forever()

    def _run_http(self):
        logger.debug("Webfront engine(HTTP) is running...")

        self._http_listener = WSGIServer(
            (self.listen_addr, self.listen_port),
            dispatcher)

        logger.debug("Webfront engine(HTTP) is listening on port: %d",
                     self._http_listener.address[1])

        self._http_listener.serve_forever()
