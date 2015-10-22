# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
from ava.runtime import environ
import logging
from .bottle import request, response, HTTPError, static_file as _static_file


logger = logging.getLogger(__name__)


static_folder = os.path.join(environ.pod_dir(), 'webroot')


def _raise_unauthorized(desc=b'Authentication required.'):
    raise HTTPError(401, desc)


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


