# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

import logging
from ..core import get_core_context
from ava.runtime import environ

from .bottle import request, response, HTTPError, static_file as _static_file
from .defines import WEBFRONT_CONTEXT_NAME

logger = logging.getLogger(__name__)


static_folder = os.path.join(environ.pod_dir(), 'webroot')


def get_webfront_engine():
    return get_core_context().lookup(WEBFRONT_CONTEXT_NAME)


def raise_unauthorized(desc=b'Authentication required.'):
    raise HTTPError(401, desc)


def get_access_token():
    return get_webfront_engine().access_token


def require_auth(callback):

    def wrapper(*args, **kwargs):
        auth = request.get_header('Authorization')
        logger.debug("Authorization: %s", auth)

        if get_webfront_engine().access_token != auth:
            logger.warning("Access token mismatched.")
            raise_unauthorized()

        body = callback(*args, **kwargs)
        return body

    return wrapper


def static_file(filepath, root=static_folder, mimetype='auto', download=False, charset='utf-8'):
    return _static_file(filepath, root=root, mimetype=mimetype, download=download, charset=charset)


def swap_root_app(wsgiapp):
    """ Swap the root WSGI application.

    :param wsgiapp:
    :return: the previous WSGI application.
    """
    from .webfront import dispatcher
    old_app = dispatcher.app
    dispatcher.app = wsgiapp

    return old_app


def set_cors_headers():
    """
    Set CORS headers
    """
    if request.method == 'GET':
        response.set_header(b'Access-Control-Allow-Origin', b'*')
        return

    if request.method == 'OPTIONS':
        response.set_header(b'Access-Control-Allow-Methods',
                            b'GET, PUT, HEAD, DELETE, OPTIONS')
        response.set_header(b'Access-Control-Allow-Headers',
                            b'authorization')

    client_origin = request.get_header(b'Origin', b'*')
    # for PUT and DELETE operations, echo back the given Origin header.
    response.set_header(b'Access-Control-Allow-Origin', client_origin)


__all__ = ['raise_unauthorized', 'static_file',
           'swap_root_app', 'set_cors_headers', 'get_webfront_engine',
           'get_access_token']
