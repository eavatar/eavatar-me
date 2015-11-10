# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from webpages import *

@pytest.fixture
def page(browser, server_url, access_token):
    return FrontPage(browser, server_url, access_token)


class TestFrontPage(object):

    def test_should_find_page_div(self, page):
        page.open()
        div = page.find_element_by_id('front')
        assert div is not None

        header = page.find_element_by_tag_name('h1')
        # time.sleep(5)
        # print(header.text)
        assert 'EAvatar ME' in header.text

    def test_can_login_and_logout(self, page):
        page.open()

        page.assert_front_page()

        token_input = page.find_element_by_xpath("//input[@name='token']")
        token_input.send_keys(page.access_token)

        login_btn = page.find_element_by_id('loginBtn')
        # page.sleep(3)
        login_btn.click()
        header2 = page.find_element_by_tag_name('h1')
        assert header2 is not None
        # print("Header:", header2.text)
        assert 'EAvatar' in header2.text

        page.logout()
        # page.sleep(120)
        # page.assert_front_page()
