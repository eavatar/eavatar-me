# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ava.task import action


import requests


@action
def head(url, **kwargs):
    return requests.head(url, **kwargs)


@action
def get(url, params=None, **kwargs):
    return requests.get(url, params, **kwargs)


@action
def post(url, data=None, json=None, **kwargs):
    return requests.post(url, data, json, **kwargs)


@action
def put(url, data=None, **kwargs):
    return requests.put(url, data, **kwargs)


@action
def patch(url, data=None, **kwargs):
    return requests.patch(url, data, **kwargs)


@action
def delete(url, **kwargs):
    return requests.delete(url, **kwargs)
