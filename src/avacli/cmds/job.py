# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import click

from .cli import cli


def _handle_list(ctx, client):
    r = client.get('/jobs')
    result = r.json()

    if result['status'] == 'error':
        click.echo(result['reason'])
        return

    for it in result['data']:
        click.echo("%s: %s:%s" % (it['id'], it['name'], it['st']))


@cli.command()
@click.argument('op', default='list')
@click.pass_context
def job(ctx, op):
    """ Running job handling.
    """
    client = ctx.obj['client']
    if op == 'list':
        _handle_list(ctx, client)
