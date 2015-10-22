# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .bottle import route, get, post, delete, put, request, response
from .bottle import HTTPError
from .bottle import Bottle as create_app


from .webfront import dispatcher
from .service import *
