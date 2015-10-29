# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from selenium import webdriver
from ava.util.tests import AgentTest

from webpages import *


class TestScriptsPage(PageTest):

    def setUp(self):
        super(TestScriptsPage, self).setUp()
        self.page = ScriptsPage(self.browser, self.live_server_url, self.access_token)

    def test_should_find_page_div(self):
        self.page.open()
        div = self.browser.find_element_by_id('scripts')
        assert div is not None
