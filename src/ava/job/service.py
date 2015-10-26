# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


from ..core import get_core_context

from .defines import ENGINE_NAME


def get_job_engine():
    return get_core_context().lookup(ENGINE_NAME)


__all__ = ['get_job_engine']
