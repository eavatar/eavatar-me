# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from selenium import webdriver
from ava.util.tests import AgentTest

from webpages import *


class TestHomePage(PageTest):

    def setUp(self):
        super(TestHomePage, self).setUp()
        self.home_page = HomePage(self.browser, self.live_server_url, self.access_token)

    def test_should_find_page_div(self):
        self.home_page.open()
        div = self.browser.find_element_by_id('home')
        assert div is not None
