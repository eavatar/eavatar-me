# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import collections
import calendar
import heapq
import bisect
import array
import Queue

import string
import re

import math
import random

import json
import lxml
import base64
import binascii
import hashlib
import hmac


def populate_scope(scope):
    """ Populates scope with basic libraries.

    :param scope: the dict
    """
    scope['datetime'] = datetime
    scope['collections'] = collections
    scope['calendar'] = calendar
    scope['heapq'] = heapq
    scope['bisect'] = bisect
    scope['array'] = array
    scope['queue'] = Queue
    scope['Queue'] = Queue  # some may be more familiar with this naming
    scope['string'] = string
    scope['re'] = re
    scope['math'] = math
    scope['random'] = random
    scope['json'] = json
    scope['lxml'] = lxml
    scope['base64'] = base64
    scope['binascii'] = binascii
    scope['hashlib'] = hashlib
    scope['hmac'] = hmac


__all__ = ['populate_scope']
