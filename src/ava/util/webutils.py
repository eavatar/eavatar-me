# -*- coding: utf-8 -*-
"""
Utility routines for web-related operations.
"""
from __future__ import print_function, division, absolute_import

import logging
import hashlib


from ..util import resource_path


static_folder = resource_path('static')

logger = logging.getLogger(__name__)

_ext_to_media_type = {
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.ico': 'image/vnd.microsoft.icon',
    '.svg': 'image/svg+xml',
    '.txt': 'text/plain',
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
}

_default_media_type = 'application/octet-stream'


def calc_etag(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()


def guess_media_type(ext):
    t = _ext_to_media_type.get(ext)
    if t is None:
        return _default_media_type
    else:
        return t
