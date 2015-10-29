# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from datetime import datetime

from ava.util.clock import clock

from ava import log
from ava.job import get_job_engine
from ava import data
from ava.user import Notice
from ava.job import Script
from ava.web.bottle import response, request, HTTPError

from .dispatcher import dispatcher
from .bottle import Bottle
from .service import require_auth, require_json, get_access_token
from . import defines as D


_logger = logging.getLogger(__name__)

api = Bottle()

dispatcher.mount('/api', api)

job_engine = get_job_engine()
notice_store = data.get_store('notices')
script_store = data.get_store('scripts')


def _not_found_error(reason='Resource not found.'):
    response.status = D.HTTP_STATUS_NOT_FOUND
    return dict(status=D.ERROR, reason=reason)


@api.route("/ping")
def ping():
    """ Simple ping test
    """
    return dict(status=D.SUCCESS)


@api.route("/auth")
@require_auth
def auth():
    print("Authenticated")
    return dict(status=D.SUCCESS, token=get_access_token())


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
    return dict(data=entries, status=D.SUCCESS)


# jobs
@api.route("/jobs")
@require_auth
def job_list():
    jobs = get_job_engine().jobs.values()

    entries = []
    for it in jobs:
        rec = dict(id=it.id, name=it.name, st=it.started_time_iso)
        entries.append(rec)

    return dict(data=entries, status=D.SUCCESS)


@api.route("/jobs", method=['POST'])
@require_json
@require_auth
def job_create():
    _logger.debug("job_create")
    data = request.json
    print("job_create: DATA: ", data)
    return dict(status=D.SUCCESS)


@api.route("/jobs/<job_id>")
@require_auth
def job_delete(job_id):
    job_engine.cancel_job(job_id)
    return dict(status=D.SUCCESS)


# Scripts
@api.route("/scripts", method='GET')
@require_auth
def script_list():
    result = []
    s = Script(title="Check GMail every 1 minute", text="script contents", auto_start=True)
    result.append(s.to_dict())
    # with script_store.cursor() as cur:
    #    for k in cur.iternext(keys=True, values=True):
    #        rec = cur.value()
    #        result.append(rec[0])
    return dict(status=D.SUCCESS, data=result)


@api.route("/scripts", method=['POST'])
@require_json
@require_auth
def script_create():

    d = request.json

    if d.get('id') is not None:
        response.status = D.HTTP_STATUS_BAD_REQUEST
        return dict(status=D.ERROR, reason="Invalid data.")

    script = Script(**d)
    assert script.id is not None

    script_store[script.id] = [script.to_dict(), clock.tick()]

    return dict(status=D.SUCCESS, data=script.id)


@api.route("/scripts/<script_id>", method=['PUT'])
@require_json
@require_auth
def script_update(script_id):
    rec = script_store.get(script_id)
    if rec is None:
        return _not_found_error("Script not found")

    script = Script(**rec[0])
    script.update(request.json)
    script_store[script.id] = [script.to_dict(), clock.tick()]

    return dict(status=D.SUCCESS, data=script_id)


@api.route("/scripts/<script_id>", method=['GET'])
@require_auth
def script_get(script_id):
    _logger.debug("Fetching script: %s", script_id)

    rec = script_store.get(script_id)
    if rec is None:
        return _not_found_error("Script not found")

    return dict(status=D.SUCCESS, data=rec[0])


@api.route("/scripts/<script_id>", method=['DELETE'])
@require_auth
def script_remove(script_id):
    rec = script_store.get(script_id)
    if rec is None:
        return _not_found_error("Script not found")

    script_store.remove(script_id)
    return dict(status=D.SUCCESS, data=script_id)


# Notices
@api.route("/notices", method=['GET'])
@require_auth
def notice_list():
    result = []

    count = 100
    with notice_store.cursor() as cur:
        for k in cur.iterprev(keys=True, values=True):
            rec = cur.value()
            result.append(rec[0])
            count -= 1
            if count == 0:
                break

    return dict(status=D.SUCCESS, data=result)


@api.route("/notices/<notice_id>", method=['DELETE'])
@require_auth
def notice_delete(notice_id):
    _logger.debug("Delete notice with ID: %s", notice_id)

    rec = notice_store.get(notice_id)
    if rec is None:
        response.status_code = 404
        return dict(status=D.ERROR, reason="Notice not found")

    notice_store.remove(notice_id)

    return dict(status=D.SUCCESS, data=notice_id)
