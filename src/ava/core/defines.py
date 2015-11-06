# -*- coding: utf-8 -*-
"""
Various definitions used across different packages.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import VERSION_STRING


# return as the root resource.
AGENT_INFO = {
    "EAvatar": "A versatile agent.",
    "version": VERSION_STRING,
    "vendor": {
        "name": "EAvatar Technology Ltd.",
        "version": VERSION_STRING
    },
}


# activated engines

INSTALLED_ENGINES = [
    "ava.log.engine:LogEngine",
    "ava.data.engine:DataEngine",
    "ava.task.engine:TaskEngine",
    "ava.mod.engine:ModuleEngine",
    "ava.user.engine:UserEngine",
    "ava.job.engine:JobEngine",
    "ava.web.webfront:WebfrontEngine",
    "ava.web.websocket:WebsocketEngine",
]


##### Environment variable ####
AVA_POD_FOLDER = 'AVA_POD'  # where the working directory.
AVA_AGENT_SECRET = 'AVA_AGENT_SECRET'  # the agent's own secret key.
AVA_SWARM_SECRET = 'AVA_SWARM_SECRET'  # the swarm's secret key.
AVA_USER_XID = 'AVA_USER_XID'  # the user's XID.


# tries to import definitions from the global settings.

try:
    from ava_settings import *
except ImportError:
    pass
