# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


import logging
import click

from ava import APP_NAME

click.disable_unicode_literals_warning = True


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.getLogger(__name__)


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    """ The command-line interface for Ava.
    """
    ctx.obj = dict(verbosity=verbose)

    log_level = logging.WARNING

    if verbose > 1:
        log_level = logging.DEBUG
    elif verbose == 1:
        log_level = logging.INFO
