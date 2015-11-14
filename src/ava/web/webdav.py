# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging

from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp

from ava.runtime import environ
from ava.web.webfront import dispatcher
from ava.web import get_webfront_engine

from .ava_dav_provider import FilesystemProvider

_logger = logging.getLogger(__name__)


class WebDavEngine(object):
    """ For launching the WebDav """

    def __init__(self):
        _logger.debug("WebDav engine created.")
        self._token = None

    def start(self, ctx):
        _logger.debug('Starting WebDAV engine...')

        self._token = get_webfront_engine().access_token

        root_folder = environ.get_app_dir()
        if isinstance(root_folder, unicode):
            root_folder = root_folder.encode('utf-8')
        provider = FilesystemProvider(root_folder)
        conf = DEFAULT_CONFIG.copy()
        conf.update({
            "mount_path": '/dav',
            "provider_mapping": {'/': provider},
            "port": 5080,
            "user_mapping": {"/": {"avame": {"password": self._token,
                                                 "description": "",
                                                 "roles": [],
                                                 },
                                       },
                             },
            "verbose": 1,
            "propsmanager": True,
            "locksmanager": True,
            'dir_browser': {
                "enable": False,
                "response_trailer": '',
                "davmount": False,
                "ms_mount": False,
                "ms_sharepoint_plugin": True,
                "ms_sharepoint_urls": False,
            },
        })

        dav_app = WsgiDAVApp(conf)
        dispatcher.mount('/dav', dav_app)

        _logger.debug("WebDav engine started.")

    def stop(self, ctx):
        _logger.debug("WebDav engine stopped.")
