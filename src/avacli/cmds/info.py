# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


import click

from .cli import cli
from ava import __version__


@cli.command()
@click.pass_context
def info(ctx):
    """ Show version information.

    :return:
    """
    click.echo("EAvatar ME V. %s" % __version__)
    click.echo("Agent URL: %s" % ctx.obj['url'])

