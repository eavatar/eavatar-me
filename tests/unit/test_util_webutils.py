# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ava.util.webutils import calc_etag, guess_media_type


def test_calc_etag():

    etag = calc_etag(b'1234')
    assert '81dc9bdb52d04dc20036dbd8313ed055' == etag


def test_guess_known_media_type():
    assert guess_media_type('.js') == 'application/javascript'


def test_guess_unknown_media_type():
    assert guess_media_type('.noexist') == 'application/octet-stream'