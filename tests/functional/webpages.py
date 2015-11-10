# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import time
import pytest
from selenium import webdriver

@pytest.fixture(scope='module')
def webfront(agent):
    return agent.context().lookup('webfront')


@pytest.fixture(scope='module')
def server_url(webfront):
    return webfront.local_base_url

@pytest.fixture(scope='module')
def access_token(webfront):
    return webfront.access_token

@pytest.fixture
def browser(request):
    browser_type = os.environ.get('AVA_TEST_BROWSER', 'Firefox')

    if browser_type == 'PhantomJS':
        b = webdriver.PhantomJS()
    else:
        b = webdriver.Firefox()

    b.implicitly_wait(5)

    def teardown_browser():
        b.quit()
    request.addfinalizer(teardown_browser)

    return b


class WebPage(object):

    def __init__(self, browser, base_url, access_token=None):
        self.browser = browser
        self.base_url = base_url
        self.access_token = access_token

    def open(self):
        self.browser.get(self.base_url)

    def login(self):
        self.browser.get(self.base_url + '#login/' + self.access_token)
        header = self.find_element_by_tag_name('h1')
        assert 'Console' in header.text

    def find_element_by_id(self, elmt_id):
        return self.browser.find_element_by_id(elmt_id)

    def find_elements_by_id(self, elmt_id):
        return self.browser.find_elements_by_id(elmt_id)

    def find_element_by_tag_name(self, tag_name):
        return self.browser.find_element_by_tag_name(tag_name)

    def find_elements_by_tag_name(self, tag_name):
        return self.browser.find_elements_by_tag_name(tag_name)

    def find_element_by_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath)

    def find_elements_by_xpath(self, xpath):
        return self.browser.find_elements_by_xpath(xpath)

    def sleep(self, secs):
        time.sleep(secs)

    def assert_home_page(self):
        header = self.find_element_by_tag_name('h1')
        assert 'Console' in header.text


class RootPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(RootPage, self).__init__(*args, **kwargs)


class ConsolePage(WebPage):

    def __init__(self, *args, **kwargs):
        super(ConsolePage, self).__init__(*args, **kwargs)

    def open(self):
        self.login()


class NoticesPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(NoticesPage, self).__init__(*args, **kwargs)

    def open(self):
        self.login()
        link = self.browser.find_element_by_xpath("//a[@href='#notices']")
        link.click()


class ScriptsPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(ScriptsPage, self).__init__(*args, **kwargs)

    def open(self):
        self.login()
        link = self.browser.find_element_by_xpath("//a[@href='#scripts']")
        link.click()


class JobsPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(JobsPage, self).__init__(*args, **kwargs)

    def open(self):
        self.login()
        link = self.browser.find_element_by_xpath("//a[@href='#jobs']")
        print("Jobs link found!")
        link.click()


class LogsPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(LogsPage, self).__init__(*args, **kwargs)

    def open(self):
        self.login()
        link = self.browser.find_element_by_xpath("//a[@href='#logs']")
        link.click()


class OptionsPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(OptionsPage, self).__init__(*args, **kwargs)

    def open(self):
        self.login()

        # click the 'Recent Logs' button

