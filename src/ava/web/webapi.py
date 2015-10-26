# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
from datetime import datetime
from ava import log
from ava.job import get_job_engine
from ava.web.bottle import response

from .dispatcher import dispatcher
from .bottle import Bottle
from .service import require_auth, get_access_token

api = Bottle()

dispatcher.mount('/api', api)


@api.route("/")
@require_auth
def hello():
    return "Hello"


@api.route("/auth")
@require_auth
def auth():
    print("Authenticated")
    return dict(status="success", token=get_access_token())

# logs
@api.route("/logs")
@require_auth
def log_list():
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


# jobs
@api.route("/jobs")
@require_auth
def job_list():
    jobs = get_job_engine().jobs.values()

    entries = []
    for it in jobs:
        rec = dict(id=it.id, name=it.name, st=it.started_time_iso)
        entries.append(rec)

    return dict(data=entries, status='success')
