# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from webpages import *

@pytest.fixture
def page(browser, server_url, access_token):
    return NoticesPage(browser, server_url, access_token)


class TestNoticesPage(object):

    def test_should_find_page_div(self, page):
        page.open()
        div = page.find_element_by_id('notices')
        assert div is not None

