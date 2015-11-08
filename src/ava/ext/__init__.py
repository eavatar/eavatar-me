# -*- coding: utf-8 -*-
"""
Extension engine is responsible for adding packages(in egg format) to the path,
and then starting or stopping extensions.

Some packages provides no extension but acts as libraries for other packages.
"""

# flake8: noqa

from __future__ import absolute_import, print_function, unicode_literals

from .service import *
