# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import click


from .cli import cli

logger = logging.getLogger(__name__)


@cli.command()
@click.pass_context
def run(ctx):
    """ Run the agent

    """
    from ava.core.agent import start_agent
    if ctx.obj['verbosity'] > 1:
        logger.debug("Starting the shell...")

    start_agent()

    if ctx.obj['verbosity'] > 1:
        logger.debug("Shell stopped.")
