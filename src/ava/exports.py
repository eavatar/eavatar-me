# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# flake8: noqa
# import packages/modules that custom modules can access

import os
import sys
import re
import ftplib
import poplib
import imaplib
import nntplib
import smtplib
import telnetlib
import logging
import logging.config
import sqlite3
import _sqlite3
import uuid
import urlparse
import webbrowser

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

import xml.etree
from xml.etree import ElementTree

import requests
from bs4 import BeautifulSoup

# Bottle framework
import bottle
from bottle import Request, Response, HTTPError

import wsgidav
from wsgidav import wsgidav_app

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
import ava.web.websocket
import ava.web.webdav

# Avame
import avame

import avashell.tui.shell

