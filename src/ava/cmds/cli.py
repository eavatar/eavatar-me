# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


import os
import sys
import glob
import logging
import click
from importlib import import_module

from ava import APP_NAME
from ava.runtime import environ

click.disable_unicode_literals_warning = True

_MODULES_DIR = os.path.join('mods', 'commands')

# the package name for modules.
_MODULE_PKG = 'mods.commands.'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.getLogger(__name__)

_modules_path = os.path.join(environ.pod_dir(), _MODULES_DIR)
_modules_path = os.path.abspath(_modules_path)
_modules = {}


def _scan_modules():
    pattern = os.path.join(_modules_path, '[a-zA-Z][a-zA-Z0-9_]*.py')
    return glob.glob(pattern)


def load_commands():
    sys.path.append(environ.pod_dir())
    # logger.debug("Command module directory: %s", _modules_path)

    module_files = _scan_modules()

    # logger.debug("Found %d command module(s)" % len(module_files))

    for s in module_files:
        name = os.path.basename(s)
        if '__init__.py' == name:
            continue

        # gets the basename without extension part.
        name = os.path.splitext(name)[0]
        try:
            # logger.debug("Loading command module: %s", name)
            mod = import_module(_MODULE_PKG + name)
            _modules[name] = mod
        except ImportError:
            logger.error("Failed to import command module: %s",
                         name,
                         exc_info=True)


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

    app_dir = click.get_app_dir(APP_NAME)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir, 0700)
    if verbose > 2:
        click.echo("Location for configuration files: %s" % app_dir)

    ctx.obj['app_dir'] = app_dir

    if ctx.invoked_subcommand is None:
        from ava.cmds.agent import run
        ctx.invoke(run)


def main():
    return cli(auto_envvar_prefix=b'AVA')

if __name__ == '__main__':
    sys.exit(main())
