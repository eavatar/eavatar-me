# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function


import logging
import click

from ava import APP_NAME
from .client import AvaClient

click.disable_unicode_literals_warning = True


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.getLogger(__name__)


@click.group(invoke_without_command=False, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.option('--url', envvar='URL', default='http://127.0.0.1:5080')
@click.option('--token', envvar='TOKEN', required=True)
@click.pass_context
def cli(ctx, verbose, url, token):
    """ The command-line interface for EAvatar ME.
    """
    ctx.obj = dict(verbosity=verbose)
    ctx.obj['url'] = url
    ctx.obj['token'] = token
    ctx.obj['client'] = AvaClient(token=token, url=url + '/api')

    log_level = logging.WARNING
    if verbose > 1:
        log_level = logging.DEBUG
    elif verbose == 1:
        log_level = logging.INFO
