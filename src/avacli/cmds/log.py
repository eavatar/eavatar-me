# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


import click

from .cli import cli

def _level_to_name(lvl):

    if lvl <= 20:
        return 'INFO'
    elif lvl <=30:
        return 'ALERT'
    else:
        return 'ERROR'


def _handle_list(ctx, client):
    r = client.get('/logs')
    result = r.json()
    if result['status'] == 'error':
        click.echo(result['reason'])
        return

    for item in result['data']:
        level_name = _level_to_name(item['lvl'])
        click.echo("%s - %s - %s" % (item['ts'], level_name, item['msg']))


@cli.command()
@click.argument('op', default='list')
@click.pass_context
def log(ctx, op):
    """ Display recent log entries.
    """
    client = ctx.obj['client']
    if op == 'list':
        _handle_list(ctx, client)
