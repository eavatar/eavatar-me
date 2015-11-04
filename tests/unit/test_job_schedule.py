# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pytest
from ava.job.schedule import Schedule


def test_schedule_seconds():

    count = 2
    for it in Schedule().every(1).second:
        print(it)
        count -= 1
        if count <= 0:
            break


def test_singular_unit():

    with pytest.raises(AssertionError):
        for it in Schedule().every(2).second:
            pass

    with pytest.raises(AssertionError):
        for it in Schedule().every(2).minute:
            pass

    with pytest.raises(AssertionError):
        for it in Schedule().every(2).hour:
            pass

    with pytest.raises(AssertionError):
        for it in Schedule().every(2).day:
            pass
