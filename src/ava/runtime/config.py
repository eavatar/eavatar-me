# -*- coding: utf-8 -*-

"""
Configuration file reading/writing.
"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os
import codecs
import logging
import logging.config
import os.path
import json

from string import Template

try:
    import ava_settings
except ImportError:
    ava_settings = None

from ..runtime import environ


AGENT_CONF = os.path.join(environ.conf_dir(), u'ava.json')

# The default configuration file is located at the base directory.

locations = dict(base_dir=environ.base_dir().replace("\\", "/"),
                 conf_dir=environ.conf_dir().replace("\\", "/"),
                 data_dir=environ.data_dir().replace("\\", "/"),
                 pkgs_dir=environ.pkgs_dir().replace("\\", "/"),
                 logs_dir=environ.logs_dir().replace("\\", "/"),
                 mods_dir=environ.mods_dir().replace("\\", "/"),
                 )

settings = dict(locations)

if ava_settings is not None:
    for attr_name in dir(ava_settings):
        if attr_name.isupper():
            settings[attr_name] = getattr(ava_settings, attr_name)


def load_conf(conf_file):
    if not os.path.exists(conf_file):
        return {}

    with codecs.open(conf_file, 'rb', encoding='utf-8') as f:
        data = f.read()
    if len(data.strip()) == 0:
        return {}

    template = Template(data)
    data = template.substitute(**locations)
    return json.loads(data)


def save_conf(conf_file, content):
    with codecs.open(conf_file, 'wb', encoding='utf-8') as out:
        os.chmod(conf_file, 0600)
        out.write(json.dumps(content, skipkeys=True, indent=2))

if settings['DEBUG']:
    print("Configuration file:", AGENT_CONF)

settings.update(load_conf(AGENT_CONF))

# configure logging
logging.config.dictConfig(settings['LOGGING'])


