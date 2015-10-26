# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
from datetime import datetime
from ava import log
from ava.web.bottle import response

from .dispatcher import dispatcher
from .bottle import Bottle

api = Bottle()

dispatcher.mount('/api', api)


@api.route("/")
def hello():
    return "Hello"


# logs
@api.route("/logs")
def get_logs():
    entries = []
    i = 1
    for it in log.recent_log_entries():
        isotime = datetime.isoformat(it.time)
        rec = dict(id=i, msg=it.message, lvl=it.levelno, ts=isotime)
        entries.append(rec)
        i += 1
    #response.content_type = b'application/json'
    # return json.dumps(entries)
    return dict(data=entries, status='success')


