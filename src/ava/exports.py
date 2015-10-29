# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


# import packages/modules that custom modules can access

import os
import sys
import logging
import logging.config
import sqlite3
import _sqlite3

# workaround for missing codec in Tiny core linux
from encodings import hex_codec, ascii, utf_8, utf_32
from click import group, command

#import ws4py
#from ws4py.server import geventserver
import wsaccel

# gevent
import gevent

# messagepack
import msgpack

# lmdb
import lmdb

# libnacl
#import libnacl
#from libnacl import _get_nacl

# lxml
import lxml
from lxml import etree

import xml.etree
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup

# Ava
import ava.wrapper
import ava.job.engine
import ava.data.engine
import ava.ext.engine
import ava.task.engine
import ava.log.engine
import ava.mod.engine
import ava.user.engine
import ava.runtime
import ava.util
import ava.web.webfront

# Avame
import avame
