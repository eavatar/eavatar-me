# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from webpages import *


class TestRootPage(PageTest):

    def setUp(self):
        super(TestRootPage, self).setUp()
        self.root_page = RootPage(self.browser, self.live_server_url, self.access_token)

    def test_should_show_a_dialog_when_opened(self):
        self.root_page.open()

        header = self.browser.find_element_by_tag_name('h1')
        # time.sleep(5)
        print(header.text)
        assert 'EAvatar ME' in header.text
