# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from webpages import *

@pytest.fixture
def page(browser, server_url, access_token):
    return JobsPage(browser, server_url, access_token)


class TestJobsPage(object):

    def test_should_find_page_div(self, page, browser):
        page.open()
        div = browser.find_element_by_id('jobs')
        assert div is not None
