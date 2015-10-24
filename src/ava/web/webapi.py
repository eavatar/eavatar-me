# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .dispatcher import dispatcher
from .bottle import Bottle

api = Bottle()

dispatcher.mount('/api', api)


@api.route("/")
def hello():
    return "Hello"
