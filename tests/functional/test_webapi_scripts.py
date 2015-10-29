# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import requests

from ava.util.tests import AgentTest


SUCCESS = 'success'
ERROR = 'error'


class TestScriptsEndpoint(AgentTest):
    # api_url = 'http://127.0.0.1:5080/api'
    api_url = ''
    access_token = None
    headers = None

    @classmethod
    def setUpClass(cls):
        # AgentTest.setUpClass()
        super(TestScriptsEndpoint, cls).setUpClass()
        webfront = cls.agent.context().lookup('webfront')
        cls.api_url = webfront.local_base_url + 'api'
        cls.access_token = webfront.access_token
        cls.headers = {'Authorization': cls.access_token,
                       'Content-type': 'application/json'}

    def test_get_scripts(self):
        url = self.api_url + '/scripts'
        r = requests.get(url, headers=self.headers)

        assert r.status_code == 200

    def test_create_script_with_wrong_content_type(self):
        url = self.api_url + '/scripts'
        myheaders = dict(self.headers)
        myheaders['Content-type'] = 'text/html'

        data = dict(text='ava.sleep(0.1)')
        r2 = requests.post(url, headers=myheaders, data=data)
        assert r2.status_code == 415

    def test_script_operations(self):
        url = self.api_url + '/scripts'
        data = dict(text='ava.sleep(0.1)', title='script1')

        # create
        r1 = requests.post(url, headers=self.headers, data=json.dumps(data))
        assert r1.status_code == 200
        script_id = r1.json().get('data')
        assert script_id is not None

        # ensure created successfully
        r2 = requests.get(url + '/' + script_id, headers=self.headers)
        assert r2.status_code == 200
        r2_data = r2.json().get('data')
        assert script_id == r2_data.get('id')
        assert 'script1' == r2_data.get('title')
        assert 'ava.sleep(0.1)' == r2_data.get('text')
        assert not r2_data['auto_start']

        del r2_data['id']

        # update
        r2_data['title'] = 'script1_1'
        r3 = requests.put(url + '/' + script_id, headers=self.headers,
                          data=json.dumps(r2_data))

        # ensure updated correctly.
        assert r3.status_code == 200
        r3_res = requests.get(url + '/' + script_id, headers=self.headers)
        assert 'script1_1' == r3_res.json()['data']['title']

        # remove
        r4 = requests.delete(url + '/' + script_id, headers=self.headers)
        assert r4.status_code == 200

        # should be removed.
        r4_res = requests.get(url + '/' + script_id, headers=self.headers)
        assert r4_res.status_code == 404

