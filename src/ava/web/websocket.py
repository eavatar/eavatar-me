# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from .webfront import dispatcher
from ws4py.websocket import WebSocket
from ws4py.server.wsgiutils import WebSocketWSGIApplication

_logger = logging.getLogger(__name__)


class WSConnection(WebSocket):

    def __init__(self, *args, **kwargs):
        super(WSConnection, self).__init__(*args, **kwargs)
        self._authenticated = False

    def received_message(self, message):
        _logger.debug("Received message from Websocket: %r", message.data)
        self.send(message.data, message.is_binary)


class WebsocketEngine(object):

    def start(self, ctx=None):
        _logger.debug("Starting Websocket engine...")

        dispatcher.mount('/ws', WebSocketWSGIApplication(
            handler_cls=WSConnection))

        _logger.debug("Websocket engine started.")

    def stop(self, ctx=None):
        _logger.debug("Websocket engine stopped.")
