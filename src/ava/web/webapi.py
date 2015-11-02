# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from datetime import datetime

from ava.util.clock import clock

from ava import log
from ava.job import get_job_engine
from ava import data as stores
from ava.user import Notice
from ava.job import Script
from ava.job.errors import ScriptSyntaxError
from ava.web.bottle import response, request, HTTPError

from .dispatcher import dispatcher
from .bottle import Bottle
from .service import require_auth, require_json, get_access_token
from . import defines as D


_logger = logging.getLogger(__name__)

api = Bottle()

dispatcher.mount('/api', api)

job_engine = get_job_engine()


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
    try:
        job_data = request.json
    except ValueError:
        response.status = D.HTTP_STATUS_BAD_REQUEST
        return dict(status=D.ERROR, reason='No valid JSON object.')

    print("job_create: DATA: ", job_data)

    if job_data is None:
        response.status = D.HTTP_STATUS_BAD_REQUEST
        return dict(status=D.ERROR, reason='No script provided.')

    try:
        job_id = get_job_engine().submit_job(job_data)
        return dict(status=D.SUCCESS, data=job_id)
    except ScriptSyntaxError as ex:
        response.status = D.HTTP_STATUS_BAD_REQUEST
        return dict(status=D.ERROR, reason=ex.message)


@api.route("/jobs/<job_id>", method="get")
@require_auth
def job_retrieve(job_id):
    job_info = get_job_engine().jobs.get(job_id)
    if job_info is None:
        return _not_found_error("Job not found")

    data = dict(id=job_info.id, name=job_info.name, st=job_info.started_time_iso)
    return dict(status=D.SUCCESS, data=data)


@api.route("/jobs/<job_id>", method="delete")
@require_auth
def job_delete(job_id):
    job_info = get_job_engine().jobs.get(job_id)
    if job_info is None:
        return _not_found_error("Job not found")
    try:
        job_engine.cancel_job(job_id)
    finally:
        return dict(status=D.SUCCESS, data=job_id)


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
    script_store = stores.get_store('scripts')
    d = request.json

    if d.get('id') is not None:
        response.status = D.HTTP_STATUS_BAD_REQUEST
        return dict(status=D.ERROR, reason="Invalid data.")

    script = Script(**d)
    assert script.id is not None
    with script_store.cursor(readonly=False) as cur:
        cur.put(script.id, [script.to_dict(), clock.tick()])

    return dict(status=D.SUCCESS, data=script.id)


@api.route("/scripts/<script_id>", method=['PUT'])
@require_json
@require_auth
def script_update(script_id):
    script_store = stores.get_store('scripts')
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

    script_store = stores.get_store('scripts')
    rec = script_store.get(script_id)
    if rec is None:
        return _not_found_error("Script not found")

    return dict(status=D.SUCCESS, data=rec[0])


@api.route("/scripts/<script_id>", method=['DELETE'])
@require_auth
def script_remove(script_id):
    store = stores.get_store('scripts')
    rec = store.get(script_id)
    if rec is None:
        return _not_found_error("Script not found")

    store.remove(script_id)
    return dict(status=D.SUCCESS, data=script_id)


@api.route("/scripts/check", method=['POST'])
@require_json
@require_auth
def script_check():

    d = request.json
    try:
        get_job_engine().validate_script(d.get('script'))
        return dict(status=D.SUCCESS)
    except Exception as ex:
        response.status = D.HTTP_STATUS_BAD_REQUEST
        return dict(status=D.ERROR, reason=ex.message)

# Notices
@api.route("/notices", method=['GET'])
@require_auth
def notice_list():
    store = stores.get_store('notices')
    result = []

    count = 100
    with store.cursor() as cur:
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
    store = stores.get_store('notices')

    rec = store.get(notice_id)
    if rec is None:
        response.status_code = 404
        return dict(status=D.ERROR, reason="Notice not found")

    store.remove(notice_id)

    return dict(status=D.SUCCESS, data=notice_id)
