# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import requests


class AvaClient(object):

    def __init__(self, token, url):
        self._token = token
        self._url = url
        self._headers = {
            'Authorization': self._token,
        }

    def get(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.get(self._url + uri, params=params, headers=headers)

    def post(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.post(self._url, params=params, headers=headers)

    def put(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.put(self._url + uri, params=params, headers=headers)

    def delete(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.delete(self._url + uri, params=params, headers=headers)

    def head(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.head(self._url + uri, params=params, headers=headers)

    def patch(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.patch(self._url + uri, params=params, headers=headers)

    def options(self, uri, params=None, headers=None):

        if headers is None:
            headers = dict()
            headers.update(self._headers)

        return requests.options(self._url + uri, params=params, headers=headers)
