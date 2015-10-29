# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
"""
This module is responsible for importing other modules such that
they have chances to initialize before the application started.
"""

# The service API
from ava.web import webapi

# For serving web root static files
from ava.web import resources

# register actions for user module, e.g. 'user.notify'.
from avame import user
