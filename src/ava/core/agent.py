# -*- coding: utf-8 -*-
"""
The agent class acts as the kernel.
"""

from __future__ import absolute_import, division, unicode_literals

import gevent
from gevent.event import Event

import os
import sys
import logging
import importlib
import inspect
from logging import NullHandler

from Queue import Empty
from collections import OrderedDict

from pydispatch import dispatcher


# from ava.util import crypto
from . import context
from .defines import INSTALLED_ENGINES, AVA_AGENT_SECRET, AVA_SWARM_SECRET
from .signals import AGENT_STARTED, AGENT_STOPPING, AGENT_STOPPED
from .errors import AgentStopped

__ssl__ = __import__('ssl')

try:
    _ssl = __ssl__._ssl
except AttributeError:
    _ssl = __ssl__._ssl2

KEYFILE = 'ava-keys.yml'


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

__agent = None

agent_running = Event()
agent_stopped = Event()


def new_sslwrap(sock, server_side=False, keyfile=None, certfile=None,
                cert_reqs=__ssl__.CERT_NONE,
                ssl_version=__ssl__.PROTOCOL_SSLv23, ca_certs=None,
                ciphers=None):
    context = __ssl__.SSLContext(ssl_version)
    context.verify_mode = cert_reqs or __ssl__.CERT_NONE
    if ca_certs:
        context.load_verify_locations(ca_certs)
    if certfile:
        context.load_cert_chain(certfile, keyfile)
    if ciphers:
        context.set_ciphers(ciphers)

    caller_self = inspect.currentframe().f_back.f_locals['self']
    return context._wrap_socket(sock, server_side=server_side,
                                ssl_sock=caller_self)


def _mygetfilesystemencoding():
    old = sys.getfilesystemencoding

    def inner_func():
        ret = old()
        if ret is None:
            return 'utf-8'
        else:
            return ret
    return inner_func


def patch_sys_getfilesystemencoding():
    # sys.getfilesystemencoding() always returns None when frozen
    # on Ubuntu systems.
    patched_func = _mygetfilesystemencoding()
    sys.getfilesystemencoding = patched_func


def restart_later():
    if __agent.running:
        logger.warning("Agent not stopped successfully!")
    sys.exit(1)


def signal_handler(signum=None, frame=None):
    logger.debug("Received HUP signal, requests the shell to restart.")
    global __agent
    if __agent:
        __agent._stop_engines()
    sys.exit(1)


def load_class(full_class_string):
    """
    dynamically load a class from a string. e.g. 'a.b.package:classname'
    """

    class_data = full_class_string.split(":")
    module_path = class_data[0]
    class_name = class_data[1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return class_name, getattr(module, class_name)


class Agent(object):
    def __init__(self, inbox, outbox):
        logger.debug("Initializing agent...")
        global agent_running
        agent_running.clear()

        patch_sys_getfilesystemencoding()

        # in case ssl.sslwrap is gone for 2.7.9, patch it.
        if not hasattr(_ssl, 'sslwrap'):
            _ssl.sslwrap = new_sslwrap

        self._dispatcher = dispatcher
        self._inbox = inbox
        self._outbox = outbox
        self.running = False
        self.interrupted = False
        self._greenlets = []
        self._context = context.get_core_context(self)
        self._engines = OrderedDict()
        self.__agent_secret = None
        self.__agent_key = None
        self.__swarm_key = None
        self.__swarm_secret = None

        # the key derived from the swarm key and is used to encrypt data.
        self.__secret_key = None

        # self.get_security_keys()

        # if hasattr(signal, 'SIGHUP'):
        #    signal.signal(signal.SIGHUP, signal_handler)

    def stop(self):
        self.interrupted = True

    def get_agent_key(self):
        return self.__agent_key

    def get_security_keys(self):
        # XXX: PyInstaller has issue in finding DLLs while building if
        # imported directly.
        crypto = importlib.import_module('crypto', 'ava.util')

        self.__agent_secret = os.environ.get(AVA_AGENT_SECRET)
        self.__swarm_secret = os.environ.get(AVA_SWARM_SECRET)

        if self.__swarm_secret is None:
            logger.error('No swarm secret is specified!')
            raise AgentStopped('No swarm secret is specified!')

        if self.__agent_secret is None:
            logger.debug("No agent secret key is given!")
            raise AgentStopped("No agent secret key is given!")

        self.__agent_secret = crypto.string_to_secret(self.__agent_secret)
        pk, sk = crypto.generate_keypair(sk=self.__agent_secret)
        self.__agent_key = pk

        self.__swarm_secret = crypto.string_to_secret(self.__swarm_secret)
        pk, sk = crypto.generate_keypair(sk=self.__swarm_secret)
        self.__swarm_key = pk

        # symmetric encryption key for the swarm cluster.
        self.__secret_key = crypto.derive_secret_key(self.__swarm_secret,
                                                     self.__swarm_key)

    def send(self, signal=dispatcher.Any, sender=dispatcher.Anonymous,
             *args, **kwargs):
        """
        Send signal/event to registered receivers.

        :param args:
        :param kwargs:
        :return:
        """
        if signal is None:
            signal = dispatcher.Any
        if sender is None:
            sender = dispatcher.Anonymous

        self._dispatcher.send(signal, sender, *args, **kwargs)

        # dispatch this signal to the shell.

        logger.info("sending signal: %s", signal)

        if self._outbox:
            self._outbox.put_nowait((signal, kwargs))

    def connect(self, receiver, signal=dispatcher.Any, sender=dispatcher.Any):
        """
        Connect the receiver to listen for signals/events.

        :param receiver
        :param signal:
        :param sender:
        """
        if signal is None:
            signal = dispatcher.Any

        if sender is None:
            sender = dispatcher.Anonymous

        self._dispatcher.connect(receiver, signal, sender)

    def disconnect(self, receiver, signal=dispatcher.Any,
                   sender=dispatcher.Any):
        """
        Disconnect the specified receiver.

        :param receiver
        :param signal:
        :param sender:
        """
        if signal is None:
            signal = dispatcher.Any

        if sender is None:
            sender = dispatcher.Anonymous

        self._dispatcher.disconnect(receiver, signal, sender)

    def add_child_greenlet(self, child):
        self._greenlets.append(child)

    def _start_engines(self):
        for it in INSTALLED_ENGINES:
            logger.debug("Loading engine: %s", it)
            try:
                name, engine_cls = load_class(it)
                engine = engine_cls()
                self._engines[name] = engine
            except:
                logger.error("Failed to create engine.", exc_info=True)

        logger.debug("Starting engines...")
        for name, engine in self._engines.iteritems():
            try:
                # logger.debug("Starting engine: %s", name)
                engine.start(self._context)
            except:
                logger.error("Failed to start engine: %s" % name,
                             exc_info=True)

    def _stop_engines(self):
        self._context.send(signal=AGENT_STOPPING, sender=self)

        engines = self._engines.values()
        engines.reverse()
        for engine in engines:
            try:
                engine.stop(self._context)
            except:
                logger.warning("Error while stopping %r", engine)

    def _start_app(self):
        try:
            importlib.import_module("ava_startup")
        except ImportError:
            logger.error("Failed to import startup module.", exc_info=True)
            raise

    def context(self):
        return self._context

    def _on_job_submitted(self, job):
        logger.debug("New job received: ", job)
        job_engine = self._context.lookup('jobengine')
        if not job_engine:
            logger.error("No job engine configured.")
            return

        job_engine.submit_job(job)

    def _process_request(self, req):
        logger.debug("Request received: %r", req)

        cmd = req[0]
        if 'job' == cmd:
            self._on_job_submitted(req[1])
        else:
            logger.warning("Unknown request: %r", cmd)

    def run(self):
        logger.debug("Starting agent...")
        global agent_running, agent_stopped
        self._start_engines()
        self._start_app()
        self.running = True
        agent_running.set()
        logger.debug("Agent started.")

        self.send(signal=AGENT_STARTED, sender=self)

        while not self.interrupted:
            try:
                gevent.joinall(self._greenlets, timeout=0.1)
            except KeyboardInterrupt:
                logger.debug("Interrupted.")
                break

            if not self._inbox:
                continue

            try:
                req = self._inbox.get_nowait()
                if req:
                    self._process_request(req)
            except Empty:
                pass

        # stop engines in reverse order.
        self.send(signal=AGENT_STOPPING, sender=self)
        self._stop_engines()

        gevent.killall(self._greenlets, timeout=1)

        self.running = False
        agent_stopped.set()
        self.send(signal=AGENT_STOPPED, sender=self)
        logger.debug("Agent stopped.")


def start_agent(inbox, outbox):
    global __agent
    __agent = Agent(inbox, outbox)
    __agent.run()
