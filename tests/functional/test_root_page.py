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
        # print(header.text)
        assert 'EAvatar ME' in header.text

    def test_can_log_in(self, page):
        page.open()

        header = page.find_element_by_tag_name('h1')
        # time.sleep(5)
        assert 'EAvatar ME' in header.text

        token_input = page.find_element_by_xpath("//input[@name='token']")
        token_input.send_keys(page.access_token)

        login_btn = page.find_element_by_id('loginBtn')
        # page.sleep(3)
        login_btn.click()
        header2 = page.find_element_by_tag_name('h1')
        assert header2 is not None
        # print("Header:", header2.text)
        assert 'EAvatar' in header2.text
