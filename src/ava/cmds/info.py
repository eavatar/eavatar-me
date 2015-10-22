# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import click

from .cli import cli
from ava.core.defines import VERSION_STRING


@cli.command()
def version():
    """ Show version information.

    :return:
    """
    click.echo("Ava Ver. %s" % VERSION_STRING)
