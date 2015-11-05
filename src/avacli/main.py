# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Entry-point for command-line interface.
"""

import avacli.cmds
from avacli.cli import cli


def main():
    return cli(auto_envvar_prefix=b'AVAME')


if __name__ == '__main__':
    main()
