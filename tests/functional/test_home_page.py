# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from webpages import *

@pytest.fixture
def page(browser, server_url, access_token):
    return HomePage(browser, server_url, access_token)


class TestHomePage(object):

    def test_should_find_page_div(self, page):
        page.open()

        div = page.find_element_by_id('home')
        assert div is not None

    def test_user_panel_should_have_logout(self, page):
        page.open()

        btn = page.find_element_by_xpath("//a[@href='#user_panel']")
        btn.click()

        logout_btn = page.find_element_by_xpath("//a[@href='#logout']")
        logout_btn.click()

    def test_menu_panel_should_have_link_to_notice_list(self, page):
        page.open()

        btn = page.find_element_by_xpath("//a[@href='#menu_panel']")
        btn.click()

        logout_btn = page.find_element_by_xpath("//a[@href='#notices']")
        logout_btn.click()

    def test_menu_panel_should_have_link_to_job_list(self, page):
        page.open()

        btn = page.find_element_by_xpath("//a[@href='#menu_panel']")
        btn.click()

        logout_btn = page.find_element_by_xpath("//a[@href='#jobs']")
        logout_btn.click()

    def test_menu_panel_should_have_link_to_log_list(self, page):
        page.open()

        btn = page.find_element_by_xpath("//a[@href='#menu_panel']")
        btn.click()

        logout_btn = page.find_element_by_xpath("//a[@href='#logs']")
        logout_btn.click()

    def test_menu_panel_should_have_link_to_console(self, page):
        page.open()

        btn = page.find_element_by_xpath("//a[@href='#menu_panel']")
        btn.click()

        logout_btn = page.find_element_by_xpath("//a[@href='#console']")
        logout_btn.click()
