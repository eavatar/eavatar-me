# -*- coding: utf-8 -*-
"""
Various encoding/decoding helpers.
"""

from __future__ import print_function, division, absolute_import

import base64


def base64url_encode(src):
    """
    URL-safe base64 encoding without padding.

    :param src:
    :return:
    """
    return base64.urlsafe_b64encode(src).replace('=','')


def base64url_decode(src):
    """
    Decode URL-safe base64-encoded string without padding.

    :param src:
    :return:
    """
    return base64.urlsafe_b64decode(src + '=' * (len(src) % 4 ))