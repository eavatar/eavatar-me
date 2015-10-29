# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from selenium import webdriver
from ava.util.tests import AgentTest


class PageTest(AgentTest):

    @classmethod
    def setUpClass(cls):
        AgentTest.setUpClass()
        webfront = cls.agent.context().lookup('webfront')
        cls.live_server_url = webfront.local_base_url
        cls.access_token = webfront.access_token

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


class WebPage(object):

    def __init__(self, browser, base_url, access_token=None):
        self.browser = browser
        self.base_url = base_url
        self.access_token = access_token

    def open(self):
        self.browser.get(self.base_url)

    def login(self):
        self.browser.get(self.base_url + '#login/' + self.access_token)
        header = self.browser.find_element_by_tag_name('h1')
        assert 'EAvatar ME' in header.text


class RootPage(WebPage):

    def __init__(self, *args, **kwargs):
        super(RootPage, self).__init__(*args, **kwargs)


class HomePage(WebPage):

    def __init__(self, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)

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

