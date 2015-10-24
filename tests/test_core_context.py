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

    def send(self, *args, **kwargs):
        """
        Send signal/event to registered receivers.

        :param args:
        :param kwargs:
        :return:
        """
        self._dispatcher.send(*args, **kwargs)

    def connect(self, receiver, *args, **kwargs):
        """
        Connect the receiver to listen for signals/events.
        :param signal:
        :param sender:
        :return:
        """
        self._dispatcher.connect(receiver, *args, **kwargs)

    def disconnect(self, receiver, *args, **kwargs):
        """
        Disconnect the specified receiver.
        :return:
        """
        self._dispatcher.disconnect(receiver, *args, **kwargs)


@pytest.fixture
def context():
    return Context(MockAgent())


class Receiver(object):
    def __init__(self):
        self.called = False

    def __call__(self, *args, **kwargs):
        self.called = True


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
        context.send(signal=SIGNAL)
        assert receiver.called
        receiver.called = False
        context.disconnect(receiver)
        context.send(signal=SIGNAL)
        assert not receiver.called

    def test_get_core_context(self):
        agent = MockAgent()
        ctx = get_core_context(agent)
        assert ctx._agent is agent

        ctx2 = get_core_context()

        assert ctx is ctx2
