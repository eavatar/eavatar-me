# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import requests

from ava.util.tests import AgentTest


SUCCESS = 'success'
ERROR = 'error'


class TestWebAPI(AgentTest):
    # api_url = 'http://127.0.0.1:5080/api'
    api_url = ''
    access_token = None
    headers = None

    @classmethod
    def setUpClass(cls):
        AgentTest.setUpClass()
        webfront = cls.agent.context().lookup('webfront')
        cls.api_url = webfront.local_base_url + 'api'
        cls.access_token = webfront.access_token
        cls.headers = {'Authorization': cls.access_token,
                       'Content-type': 'application/json'}

    def test_ping(self):
        r = requests.get(self.api_url + '/ping')

        assert r.status_code == 200
        data = r.json()
        assert data['status'] == SUCCESS

    def test_cannot_access_without_valid_token(self):
        r = requests.get(self.api_url + '/auth')

        assert r.status_code == 401
        data = r.json()
        assert data['status'] == ERROR

    def test_can_authenticate_with_valid_token(self):
        r = requests.get(self.api_url + '/auth', headers=self.headers)

        assert r.status_code == 200
        data = r.json()
        assert data['status'] == SUCCESS
        assert data['token'] == self.access_token

    def test_notices_endpoint(self):
        url = self.api_url + '/notices'
        r = requests.get(url, headers=self.headers)

        assert r.status_code == 200

    def test_get_job_list(self):
        url = self.api_url + '/jobs'
        r = requests.get(url, headers=self.headers)

        assert r.status_code == 200

    def test_create_job_with_wrong_content_type(self):
        url = self.api_url + '/jobs'
        myheaders = dict(self.headers)
        myheaders['Content-type'] = 'text/html'

        data = dict(script='ava.sleep(0.1)')
        r2 = requests.post(url, headers=myheaders, data=data)
        assert r2.status_code == 415

    def test_job_operations(self):
        url = self.api_url + '/jobs'
        data = dict(script='ava.sleep(10)')
        r1 = requests.post(url, headers=self.headers, data=json.dumps(data))
        assert r1.status_code == 200
        job_id = r1.json().get('data')
        assert job_id is not None

        r2 = requests.get(url + '/' + job_id, headers=self.headers)
        assert r2.status_code == 200
        r2_data = r2.json().get('data')
        assert job_id == r2_data.get('id')

        # remove
        r3 = requests.delete(url + '/' + job_id, headers=self.headers)
        assert r3.status_code == 200

        # should be removed.
        r3_res = requests.get(url + '/' + job_id, headers=self.headers)
        assert r3_res.status_code == 404


    def test_logs_endpoint(self):
        url = self.api_url + '/logs'
        r = requests.get(url, headers=self.headers)

        assert r.status_code == 200


