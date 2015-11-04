# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava.task import action
from bs4 import BeautifulSoup


@action
def parse(html_text, parser='html.parser'):
    """ Use BeautifulSoup4 to parse HTML document.

    :param html_text: the HTML data
    :param parser: the type of parser to use
    :return: a BS4 parser
    """
    return BeautifulSoup(html_text, parser)
