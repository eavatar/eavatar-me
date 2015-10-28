# -*- coding: utf-8 -*-

from __future__ import print_function

import gevent
from gevent import monkey
monkey.patch_all()
from gevent.lock import RLock


import pytest
from ava.core import Context
from ava.data.engine import DataEngine


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


class TestDataEngine(object):

    def test_create_and_remove_store(self, dataengine):
        store = dataengine.get_store("testdb", create=False)
        assert store is None

        store = dataengine.create_store("testdb")
        assert store is not None

        store = dataengine.get_store("testdb")
        assert store is not None
        store2 = dataengine.get_store("testdb")
        assert store is store2

        assert "testdb" in dataengine
        store = dataengine['testdb']
        assert store is store2

        del dataengine["testdb"]
        store = dataengine.get_store("testdb", create=False)
        assert not dataengine.store_exists("testdb")

    def test_crud(self, dataengine):
        store = dataengine.create_store("testdb2")
        assert store is not None

        with dataengine.cursor("testdb2", readonly=False) as cur:
            ret1 = cur.put('doc1', 'value1')
            assert ret1
            cur.put('doc2', 'value2')
            cur.put('doc3', b"中文")

        with dataengine.cursor("testdb2") as cur:
            val1 = cur.get("doc1")
            assert "value1" == val1
            val3 = cur.get("doc3")
            assert b"中文" == val3

        with dataengine.cursor("testdb2", readonly=False) as cur:
            cur.remove("doc2")
            doc2 = cur.get("doc2")
            assert doc2 is None

        dataengine.remove_store("testdb2")

    def test_crud_with_store(self, dataengine):
        store = dataengine.create_store("testdb2")
        assert store is not None

        store['doc1'] = 'value1'
        store['doc2'] = 'value2'
        store['doc3'] = b"中文"

        assert len(store) == 3
        assert 'doc1' in store

        assert "value1" == dataengine['testdb2']['doc1']
        assert b"中文" == store['doc3']

        del store['doc2']
        assert store['doc2'] is None

        # it's ok to delete nonexistent entry
        del store['doc2']

        dataengine.remove_store("testdb2")

    def test_seek_and_seek_range(self, dataengine):
        store = dataengine.create_store("testdb2")
        assert store is not None

        store[b'doc1'] = b'value1'
        store[b'doc2'] = b'value2'
        store[b'doc3'] = b'value3'

        with dataengine.cursor("testdb2", readonly=True) as cur:
            assert cur.seek('doc2')
            assert b'doc2' == cur.key()
            assert b'value2 == cur.value'

            assert cur.seek_range('doc')
            assert b'doc1' == cur.key()
            assert not cur.seek_range('doc4')

        dataengine.remove_store("testdb2")

    def test_transaction_abort(self, dataengine):
        store = dataengine.create_store("testdb2")
        assert store is not None

        try:
            with dataengine.cursor("testdb2", readonly=False) as cur:
                cur.put('_id', "k1")
                cur.put('_id', "k2")
                raise Exception()
        except:
            pass

        with dataengine.cursor("testdb2") as cur:
            assert cur.get("k1") is None
            assert cur.get("k2") is None

        dataengine.remove_store("testdb2")

    def test_forward_iterator(self, dataengine):
        store = dataengine.create_store("testdb2")
        assert store is not None

        with dataengine.cursor("testdb2", readonly=False) as cur:
            cur.put('k1', 'value3')
            cur.put('k2', 'value1')
            cur.put('k3', 'value2')

        with dataengine.cursor("testdb2") as cur:
            cur.seek("k1")

            it = cur.iternext()
            assert "k1" == it.next()
            assert "k2" == it.next()
            assert "k3" == it.next()

        dataengine.remove_store("testdb2")

    def test_backward_iterator(self, dataengine):
        store = dataengine.create_store("testdb2")
        assert store is not None

        with dataengine.cursor("testdb2", readonly=False) as cur:
            cur.put('k1', 'value3')
            cur.put('k2', 'value1')
            cur.put('k3', 'value2')

        with dataengine.cursor("testdb2") as cur:
            cur.last()

            it = cur.iterprev()
            assert "k3" == it.next()
            assert "k2" == it.next()
            assert "k1" == it.next()

        dataengine.remove_store("testdb2")

    def test_post_and_pop(self, dataengine):
        store = dataengine.create_store("queue")
        with dataengine.cursor("queue", readonly=False) as cur:
            cur.post('v1')
            cur.post('v2')
            cur.post('v3')

        with dataengine.cursor("queue", readonly=False) as cur:
            assert 'v1' == cur.pop()
            assert 'v2' == cur.pop()
            assert 'v3' == cur.pop()
            assert cur.pop() is None

        dataengine.remove_store("queue")

    def test_concurrent_updates(self, dataengine):
        store = dataengine.create_store("queue")
        lock = RLock()

        def task1():
            print("Task1: start")
            with lock:
                with dataengine.cursor("queue", readonly=False) as cur:
                    cur.put('k1', 'value3')
                    print("Task1: k1 written.")
                    gevent.sleep(0)
                    cur.put('k2', 'value1')
                    print("Task1: k2 written.")
                    gevent.sleep(0)
                    cur.put('k3', 'value2')
                    print("Task1: k3 written.")

        def task2():
            print("Task2: start")
            with lock:
                with dataengine.cursor("queue", readonly=False) as cur2:
                    cur2.put('k4', 'value3')
                    print("Task2: k4 writen.")
                    gevent.sleep(0)
                    cur2.put('k5', 'value1')
                    print("Task2: k5 written.")
                    gevent.sleep(0)
                    cur2.put('k6', 'value2')
                    print("Task2: k6 written.")

        def task3():
            print("Task3: start")
            with dataengine.cursor("queue", readonly=True) as cur3:
                cur3.get('k1')
                print("Task3: k1 read.")
                gevent.sleep(0)
                cur3.get('k2')
                print("Task3: k2 read.")
                gevent.sleep(0)
                cur3.get('k3')
                print("Task3: k3 read.")

        t1 = gevent.spawn(task1)
        t2 = gevent.spawn(task2)
        t3 = gevent.spawn(task3)
        gevent.joinall([t1, t2, t3])
