# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ..core import AvaError


class DataError(AvaError):
    """
    Generic error related to database operations.
    """
    def __init__(self, *args, **kwargs):
        super(DataError, self).__init__(*args, **kwargs)


class DataNotFoundError(DataError):
    def __init__(self, *args, **kwargs):
        super(DataNotFoundError, self).__init__(*args, **kwargs)


class DataExistError(DataError):
    def __init__(self, *args, **kwargs):
        super(DataExistError, self).__init__(*args, **kwargs)


__all__ = ['DataError', 'DataExistError', 'DataNotFoundError']
