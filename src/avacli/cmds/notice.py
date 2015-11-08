# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


import click

from .cli import cli


def _priority_to_name(lvl):

    if lvl <= 20:
        return 'INFO'
    elif lvl <= 30:
        return 'ALERT'
    else:
        return 'ERROR'


def _handle_list(ctx, client):
    r = client.get('/notices')
    result = r.json()

    if result['status'] == 'error':
        click.echo(result['reason'])
        return

    for it in result['data']:
        priority_name = _priority_to_name(it['priority'])
        click.echo("%s: %s: %s - %s" % (it['timestamp'], priority_name, it['message'], it['title']))


@cli.command()
@click.argument('op', default='list')
@click.pass_context
def notice(ctx, op):
    """ Display user notices.
    """
    client = ctx.obj['client']
    if op == 'list':
        _handle_list(ctx, client)
