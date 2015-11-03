# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from webpages import *

@pytest.fixture
def page(browser, server_url, access_token):
    return RootPage(browser, server_url, access_token)


class TestRootPage(object):

    def test_should_show_a_dialog_when_opened(self, page):
        page.open()

        header = page.find_element_by_tag_name('h1')
        # time.sleep(5)
        print(header.text)
        assert 'EAvatar ME' in header.text
