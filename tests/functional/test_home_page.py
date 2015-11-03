# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from webpages import *


@pytest.fixture
def home_page(browser, server_url, access_token):
    return HomePage(browser, server_url, access_token)


class TestHomePage(object):
    def test_should_find_page_div(self, browser, home_page):
        home_page.open()
        div = browser.find_element_by_id('home')
        assert div is not None

    def test_can_submit_script(self, browser, home_page):
        home_page.open()
        scriptEl = browser.find_element_by_id('script')
        assert scriptEl is not None
        submitBtn = browser.find_element_by_id('submitBtn')
        msgDiv = browser.find_element_by_id('submit_message')
        assert submitBtn is not None

        scriptEl.send_keys("ava.sleep(0.1)")
        submitBtn.click()
        assert 'Job ID' in msgDiv.text


