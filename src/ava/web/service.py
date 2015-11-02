# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os

import logging
from ..core import get_core_context
from ava.runtime import environ
from ava.runtime.config import settings

from .bottle import request, response, HTTPError, static_file as _static_file
from . import defines as D



logger = logging.getLogger(__name__)


static_folder = os.path.join(environ.pod_dir(), 'webroot')


def get_webfront_engine():
    return get_core_context().lookup(D.WEBFRONT_CONTEXT_NAME)


def raise_unauthorized(desc=b'Authentication required.'):
    raise HTTPError(D.HTTP_STATUS_AUTH_REQUIRED, desc)


def get_access_token():
    return get_webfront_engine().access_token


def require_auth(callback):

    def wrapper(*args, **kwargs):
        auth = request.get_header('Authorization')

        if get_webfront_engine().access_token != auth:
            if not settings['DEBUG']:
                response.status = D.HTTP_STATUS_AUTH_REQUIRED
                response.content_type = D.JSON_CONTENT_TYPE
                return dict(status='error', reason='Authentication required.')
            else:
                logger.warning("In DEBUG mode, access token is ignored.")

        body = callback(*args, **kwargs)
        return body

    return wrapper


def require_json(callback):

    def wrapper(*args, **kwargs):
        ct = request.content_type
        logger.debug("Content-type: %s", ct)

        if ct is None:
            ct = ''
        ct.strip().lower()

        if not ct.startswith('application/json'):
            logger.warning("JSON type expected, instead received: %s", ct)
            response.status = D.HTTP_STATUS_UNSUPPORTED_TYPE
            response.content_type = D.JSON_CONTENT_TYPE
            return dict(status='error', reason='Request data type is not supported.')

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
