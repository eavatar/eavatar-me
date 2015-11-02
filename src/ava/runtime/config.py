# -*- coding: utf-8 -*-

"""
Configuration file reading/writing.
"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os
import glob
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


def load_conf_files():
    """
    Loads all files with extension '.conf' in the configuration folder.
    """
    conf_loc = locations['conf_dir']
    for f in glob.glob(os.path.join(conf_loc, '*.conf')):
        conf = load_conf(f)
        basename = os.path.basename(f)
        basename = os.path.splitext(basename)[0]

        # section names should be in upper case.
        settings[basename.upper()] = conf

# load configuration files.
load_conf_files()

# configure logging
logging.config.dictConfig(settings['LOGGING'])


