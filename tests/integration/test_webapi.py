# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import requests
import pytest


@pytest.fixture(scope='module')
def webfront(agent):
    return agent.context().lookup('webfront')

@pytest.fixture
def api_url(webfront):
    return webfront.local_base_url + 'api'


@pytest.fixture
def access_token(webfront):
    return webfront.access_token

@pytest.fixture
def headers(access_token):
    return {'Authorization': access_token,
            'Content-type': 'application/json'}

SUCCESS = 'success'
ERROR = 'error'


class TestBasics(object):

    def test_ping(self, api_url):
        r = requests.get(api_url + '/ping')

        assert r.status_code == 200
        data = r.json()
        assert data['status'] == SUCCESS

    def test_cannot_access_without_valid_token(self, api_url):
        r = requests.get(api_url + '/auth')

        assert r.status_code == 401
        data = r.json()
        assert data['status'] == ERROR

    def test_can_authenticate_with_valid_token(self, api_url, headers, access_token):
        r = requests.get(api_url + '/auth', headers=headers)

        assert r.status_code == 200
        data = r.json()
        assert data['status'] == SUCCESS
        assert data['token'] == access_token


class TestLogsEndpoint(object):
    """ /api/logs
    """
    def test_logs_endpoint(self, api_url, headers):
        url = api_url + '/logs'
        r = requests.get(url, headers=headers)

        assert r.status_code == 200


class TestNoticesEndpoint(object):
    """ /api/notices
    """
    def test_notices_endpoint(self, api_url, headers):
        url = api_url + '/notices'
        r = requests.get(url, headers=headers)

        assert r.status_code == 200


class TestJobsEndpoint(object):
    """ /api/jobs
    """
    def test_get_job_list(self, api_url, headers):
        url = api_url + '/jobs'
        r = requests.get(url, headers=headers)

        assert r.status_code == 200

    def test_create_job_with_wrong_content_type(self, api_url, headers):
        url = api_url + '/jobs'
        myheaders = dict(headers)
        myheaders['Content-type'] = 'text/html'

        data = dict(script='ava.sleep(0.1)')
        r2 = requests.post(url, headers=myheaders, data=data)
        assert r2.status_code == 415

    def test_job_operations(self, api_url, headers):
        url = api_url + '/jobs'
        data = dict(script='ava.sleep(10)')
        r1 = requests.post(url, headers=headers, data=json.dumps(data))
        assert r1.status_code == 200
        job_id = r1.json().get('data')
        assert job_id is not None

        r2 = requests.get(url + '/' + job_id, headers=headers)
        assert r2.status_code == 200
        r2_data = r2.json().get('data')
        assert job_id == r2_data.get('id')

        # remove
        r3 = requests.delete(url + '/' + job_id, headers=headers)
        assert r3.status_code == 200

        # should be removed.
        r3_res = requests.get(url + '/' + job_id, headers=headers)
        assert r3_res.status_code == 404


class TestScriptsEndpoint(object):
    """ /api/scripts
    """
    def test_get_scripts(self, api_url, headers):
        url = api_url + '/scripts'
        r = requests.get(url, headers=headers)

        assert r.status_code == 200

    def test_create_script_with_wrong_content_type(self, api_url, headers):
        url = api_url + '/scripts'
        myheaders = dict(headers)
        myheaders['Content-type'] = 'text/html'

        data = dict(text='ava.sleep(0.1)')
        r2 = requests.post(url, headers=myheaders, data=data)
        assert r2.status_code == 415

    def test_script_operations(self, api_url, headers):
        url = api_url + '/scripts'
        data = dict(text='ava.sleep(0.1)', title='script1')

        # create
        r1 = requests.post(url, headers=headers, data=json.dumps(data))
        assert r1.status_code == 200
        script_id = r1.json().get('data')
        assert script_id is not None

        # ensure created successfully
        r2 = requests.get(url + '/' + script_id, headers=headers)
        assert r2.status_code == 200
        r2_data = r2.json().get('data')
        assert script_id == r2_data.get('id')
        assert 'script1' == r2_data.get('title')
        assert 'ava.sleep(0.1)' == r2_data.get('text')
        assert not r2_data['auto_start']

        del r2_data['id']

        # update
        r2_data['title'] = 'script1_1'
        r3 = requests.put(url + '/' + script_id, headers=headers,
                          data=json.dumps(r2_data))

        # ensure updated correctly.
        assert r3.status_code == 200
        r3_res = requests.get(url + '/' + script_id, headers=headers)
        assert 'script1_1' == r3_res.json()['data']['title']

        # remove
        r4 = requests.delete(url + '/' + script_id, headers=headers)
        assert r4.status_code == 200

        # should be removed.
        r4_res = requests.get(url + '/' + script_id, headers=headers)
        assert r4_res.status_code == 404

