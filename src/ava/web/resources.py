# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
"""
Provides routines for handling static resources.
"""

import os

import bottle

from ..util import resource_path

_WEBROOT = resource_path('webfront')

_JSROOT = os.path.join(_WEBROOT, 'js')


@bottle.route('/')
@bottle.route('/index.html')
def serve_home():
    return bottle.static_file('index.html', root=_WEBROOT)


@bottle.route('/favicon.icon')
def serve_favicon():
    return bottle.static_file('favicon.ico', root=_WEBROOT)


@bottle.route('/<filename:path>')
def serve_static_files(filename):
    return bottle.static_file(filename, root=_WEBROOT)
