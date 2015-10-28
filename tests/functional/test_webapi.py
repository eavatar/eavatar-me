# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import requests

from ava.util.tests import AgentTest


SUCCESS = 'success'
ERROR = 'error'


class TestWebAPI(AgentTest):
    # api_url = 'http://127.0.0.1:5080/api'
    api_url = ''

    @classmethod
    def setUpClass(cls):
        AgentTest.setUpClass()
        webfront = cls.agent.context().lookup('webfront')
        cls.api_url = webfront.local_base_url + 'api'

    def test_ping(self):
        r = requests.get(self.api_url + '/ping')

        assert r.status_code == 200
        data = r.json()
        assert data['status'] == SUCCESS
