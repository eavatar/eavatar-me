# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class Context(object):
    """
    The core context for all other entities.
    """
    def __init__(self, agent):
        self._agent = agent
        self._attributes = {}

    def __getitem__(self, item):
        return self.lookup(item)

    def __setitem__(self, key, value):
        self.bind(key, value)

    def __delitem__(self, key):
        self.unbind(key)

    def __getattr__(self, item):
        return self.lookup(item)

    @property
    def peer_id(self):
        """ Gets the public key of the agent which is used as the peer ID.
        :return: the peer ID in bytes
        """
        return self._agent.get_agent_key()

    def bind(self, key, provider):
        """ Makes a binding to the specified key.

        :param key:
        :param provider:
        :return:
        """
        self._attributes[key] = provider

    def unbind(self, key):
        """ Removes the binding specified by the key.
        :param key: the binding key.
        """
        if key in self._attributes:
            del self._attributes[key]

    def lookup(self, key, default=None):
        """ Looks up the attribute bound the specified key.

        :param key: the key
        :param default: the default value if no value is bound
        :return: the bound value or the default value.
        """
        obj = self._attributes.get(key)
        if not obj:
            return default
        elif callable(obj):
            return obj()
        else:
            return obj

    def add_child_greenlet(self, child):
        """ Adds a greenlet to be joined when the agent stops.
        :param child: the greenlet
        """
        self._agent.add_child_greenlet(child)

    def send(self, signal=None, sender=None, *args, **kwargs):
        """
        Send signal/event to registered receivers.

        :param args:
        :param kwargs:
        :return:
        """
        self._agent.send(signal, sender, *args, **kwargs)

    def connect(self, receiver, signal=None, sender=None):
        """
        Connect the receiver to listen for signals/events.
        :param receiver
        :param signal:
        :param sender:
        """
        self._agent.connect(receiver, signal, sender)

    def disconnect(self, receiver, signal=None, sender=None):
        """
        Disconnect the specified receiver.
        :param receiver
        :param signal:
        :param sender:
        """
        self._agent.disconnect(receiver, signal, sender)

    def stop(self):
        """ Requests to stop the agent properly.
        """
        self._agent.stop()

    def encrypt(self, plaindata):
        """ Encrypt data with the swarm key
        """
        return self._agent.encrypt(plaindata)

    def decrypt(self, cipherdata):
        """
        """
        return self._agent.decrypt(cipherdata)


#  Singleton construction
_context = None


def get_core_context(agent=None):
    """
    Gets the context singleton. Must first be invoked by the agent.

    :param agent: the agent which provides the context service.
    :return: the context singleton
    """
    global _context

    # _context cannot be initialized twice, and agent must not be None if
    # _context is not yet initialized.
    if _context is None:
        assert agent is not None
        _context = Context(agent)
    else:
        assert agent is None

    return _context


__all__ = ['Context', 'get_core_context']
