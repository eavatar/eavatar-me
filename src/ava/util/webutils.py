# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import logging
import hashlib
try:
    from urllib2 import parse_http_list as _parse_list_header
except ImportError: # pragma: no cover
    from urllib.request import parse_http_list as _parse_list_header
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


def unquote_header_value(value, is_filename=False):
    r"""Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    .. versionadded:: 0.5

    :param value: the header value to unquote.
    """
    if value and value[0] == value[-1] == '"':
        # this is not the real unquoting, but fixing this so that the
        # RFC is met will result in bugs with internet explorer and
        # probably some other browsers as well.  IE for example is
        # uploading files with "C:\foo\bar.txt" as filename
        value = value[1:-1]

        # if this is a filename and the starting characters look like
        # a UNC path, then just return the value without quotes.  Using the
        # replace sequence below on a UNC path has the effect of turning
        # the leading double slash into a single slash and then
        # _fix_ie_filename() doesn't work correctly.  See #458.
        if not is_filename or value[:2] != '\\\\':
            return value.replace('\\\\', '\\').replace('\\"', '"')
    return value


def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    """
    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)
    return result


def parse_dict_header(value):
    """Parse lists of key, value pairs as described by RFC 2068 Section 2 and
    convert them into a python dict (or any other mapping object created from
    the type with a dict like interface provided by the `cls` argugment):

    :param value: a string with a dict header.
    :param cls: callable to use for storage of parsed results.
    :return: an instance of `cls`
    """
    result = dict()
    for item in _parse_list_header(value):
        if '=' not in item:
            result[item] = None
            continue
        name, value = item.split('=', 1)
        if value[:1] == value[-1:] == '"':
            value = unquote_header_value(value[1:-1])
        result[name] = value
    return result


def parse_authorization_header(auth):
    if not auth:
        return

    try:
        auth_scheme, auth_info = auth.split(None, 1)
        auth_scheme = auth_scheme.lower()
    except ValueError:
        return

    result = parse_dict_header(auth_info)
    result['scheme'] = auth_scheme
    return result
