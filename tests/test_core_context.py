# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import pytest
from pydispatch import dispatcher
from ava.core.context import Context, get_core_context


class MockAgent(object):
    def __init__(self):
        self.greenlets = []
        self._dispatcher = dispatcher

    def add_child_greenlet(self, child):
        self.greenlets.append(child)

    def send(self, signal=dispatcher.Any, sender=dispatcher.Anonymous, *args, **kwargs):
        if signal is None:
            signal = dispatcher.Any
        if sender is None:
            sender = dispatcher.Anonymous

        self._dispatcher.send(signal, sender, *args, **kwargs)

    def connect(self, receiver, signal=dispatcher.Any, sender=dispatcher.Any):
        if signal is None:
            signal = dispatcher.Any

        if sender is None:
            sender = dispatcher.Anonymous

        self._dispatcher.connect(receiver, signal, sender)

    def disconnect(self, receiver, signal=dispatcher.Any, sender=dispatcher.Any):
        if signal is None:
            signal = dispatcher.Any

        if sender is None:
            sender = dispatcher.Anonymous


        self._dispatcher.disconnect(receiver, signal, sender)


@pytest.fixture
def context():
    return Context(MockAgent())


class Receiver(object):
    def __init__(self):
        self.called = False
        self.args = None
        self.kwargs = None

    def __call__(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs


class TestCoreContext(object):

    def test_binding_and_lookups(self, context):
        context.bind('test', 'value')
        value = context.lookup('test')
        assert value == 'value'
        context.unbind('test')
        value2 = context.lookup('test')
        assert value2 is None

    def test_send_signals(self, context):
        receiver = Receiver()
        context.connect(receiver, signal='test_event')
        context.send(signal='test_event')

        assert receiver.called

    def test_connect_and_then_disconnect(self, context):
        SIGNAL = 'my-second-signal'
        receiver = Receiver()
        context.connect(receiver)
        context.send(SIGNAL, msg="message", title="1234")
        assert receiver.called
        receiver.called = False
        print(receiver.args, receiver.kwargs)

        context.disconnect(receiver)
        context.send(signal=SIGNAL)
        assert not receiver.called

    def test_get_core_context(self):
        agent = MockAgent()
        ctx = get_core_context(agent)
        assert ctx._agent is agent

        ctx2 = get_core_context()

        assert ctx is ctx2
