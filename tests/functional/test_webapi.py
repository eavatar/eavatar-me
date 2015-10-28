# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import requests

from ava.util.tests import AgentTest


SUCCESS = 'success'
ERROR = 'error'


class TestWebAPI(AgentTest):
    api_url = 'http://127.0.0.1:5080/api'

    def test_ping(self):
        r = requests.get(self.api_url + '/ping')

        assert r.status_code == 200
        data = r.json()
        assert data['status'] == SUCCESS
