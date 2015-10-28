# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import gevent
from gevent import monkey
monkey.patch_all()
from gevent.lock import RLock


import pytest

from ava.util.clock import clock
from ava.core import Context
from ava.data.engine import DataEngine
from ava import data
from ava import user


@pytest.fixture
def dataengine(request, tmpdir):
    dir = tmpdir.mkdir("data")
    engine = DataEngine(datapath=dir.dirname)
    ctx = Context(None)
    ctx.bind('dataengine', engine)
    engine.start(ctx)
    engine.remove_all_stores()

    def cleanup():
        engine.remove_all_stores()
        engine.store_names()
    request.addfinalizer(cleanup)

    return engine

@pytest.fixture
def notice_store(dataengine):
    return dataengine.get_store('notices')


class TestNoticeStore(object):

    def test_can_save_and_load_notice(self, notice_store):
        notice = user.Notice(message='msg1', title='title1')
        rec = [notice.to_dict(), clock.tick()]
        notice_store[notice.id] = rec

        r2 = notice_store.get(notice.id)

        assert r2 is not None
        assert isinstance(r2, tuple)
        assert len(r2) == 2

        d = r2[0]

        notice2 = user.Notice(**d)

        assert notice2.id == notice.id
        assert notice2.message == notice.message



