# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Default settings which can be overridden by configuration files.
"""

EXE_NAME = 'ava'

DEBUG = True

WEBFRONT = {
    "disabled": False,
    "listen_port": 5080,
    "listen_addr": "127.0.0.1",
    "secure_listen_addr": "",
    "secure_listen_port": 5443,
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
      "simple": {
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      "console": {
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "formatter": "simple"
      },
      "file_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "INFO",
        "formatter": "simple",
        "filename": "${logs_dir}/ava.log",
        "maxBytes": 1048576,
        "backupCount": 2,
        "encoding": "utf8"
      }
    },
    "loggers": {
      "ava": {
        "level": "DEBUG",
        "handlers": [
          "console",
          "file_handler"
        ],
        "propagate": "no"
      },
      "avashell": {
        "level": "DEBUG",
        "handlers": [
          "console",
          "file_handler"
        ],
        "propagate": "no"
      },
      "root": {
        "level": "DEBUG",
        "handlers": [
          "console"
        ]
      }
    }
}
