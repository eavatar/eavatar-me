# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import os
import logging
import base58
import gevent
# from gevent.pywsgi import WSGIServer
from ws4py.server.geventserver import WSGIServer

from ava.runtime.config import settings
from ava.runtime import environ

from . import bottle

from . import dispatcher


logger = logging.getLogger(__name__)

_CONF_SECTION = 'WEBFRONT'

webfront = None


class WebfrontEngine(object):
    """
    The client-facing web interface.
    """
    def __init__(self):
        logger.debug("Initializing webfront engine...")
        global webfront
        webfront = self

        self._http_listener = None
        self._https_listener = None
        self.listen_port = 5000
        self.listen_addr = '127.0.0.1'
        self.secure_listen_port = 0  # 0 means not binding
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)
        self.secure_base_url = "https://127.0.0.1:%d/" % (self.secure_listen_port,)
        self._token = None

    @property
    def access_token(self):
        return self._token

    def _acquire_access_token(self):

        self._token = os.environ.get('AVA_ACCESS_TOKEN', base58.b58encode(os.urandom(16)))

    def start(self, ctx=None):
        logger.debug("Starting webfront engine...")

        disabled = settings[_CONF_SECTION].get('disabled')
        if disabled:
            logger.debug("Webfront is not enabled.")
            return

        self._acquire_access_token()
        logger.info("Access Token: %s", self._token)

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
