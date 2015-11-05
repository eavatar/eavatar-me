# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import click

from ..cli import cli
from ava import __version__


@cli.command()
def version():
    """ Show version information.

    :return:
    """
    click.echo("EAvatar ME V. %s" % __version__)
