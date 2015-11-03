# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from ava.task import action


@action
def hello(name=None):
    if name is None:
        print("Hello, there.")
    else:
        print("Hello, %s!" % name)

    return name
