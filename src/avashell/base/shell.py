# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import sys
import logging
import click
import Queue
from abc import abstractmethod
from threading import Thread
from collections import deque
import webbrowser

from ava import wrapper
from ava.core import get_core_context, AGENT_STOPPED
from ava.runtime import environ
from ava.user import USER_NOTIFIED, status
from ava.job import JOB_ACCEPTED, JOB_FINISHED, JOB_REJECTED, JOB_FAILED

from .defines import NUM_OF_NOTICES

_logger = logging.getLogger(__name__)


class ShellBase(object):
    def __init__(self):
        self.outbox = Queue.Queue()
        self.inbox = Queue.Queue()
        self.status = 'Ready'
        self.notices = deque(maxlen=NUM_OF_NOTICES)
        self.user_status = status.AVAILABLE

    def open_help(self):
        webbrowser.open('https://samkuo.me')  # changed to wherever your doc is

    def open_ui(self):
        url = 'http://127.0.0.1:5080/'
        webfront = get_core_context().lookup('webfront')
        if webfront is not None:
            url = webfront.local_base_url

        url += "#login/" + webfront.access_token
        webbrowser.open(url)

    def open_folder(self):
        click.launch(environ.get_app_dir())

    def should_notify(self, notice):
        return self.user_status == status.AVAILABLE

    def run(self):

        t = Thread(target=wrapper.launch, args=(self.inbox, self.outbox))
        t.setDaemon(True)
        t.start()

        self._run()

    def on_user_notified(self, notice):
        """
        :param msg: Message
        :param title: Title
        """
        print(notice.title)
        print('-' * len(notice.title))
        print(notice.message)

    def on_job_accepted(self, job_name):
        _logger.info("Job accepted: %s", job_name)

    def on_job_rejected(self, reason):
        _logger.error("Job rejected: %s", reason)

    def on_job_failed(self, job_ctx):
        _logger.error("Job '%s' cannot be done: %r", job_ctx.name,
                      job_ctx.exception)

    def on_job_finished(self, job_ctx):
        _logger.info("Job '%s' finished.", job_ctx.name)

    def on_agent_stopped(self):
        self._terminate()

    def get_notice_at(self, index):
        # reserved index
        return self.notices[-(index + 1)]

    def set_status(self, status):
        self.status = status

    def submit_job(self, job):
        self.inbox.put_nowait(('job', job))

    def process_idle_tasks(self):
        # _logger.debug("Processing idle tasks...")

        try:
            item = self.outbox.get_nowait()
            event = item[0]
            # handle the request
            _logger.debug("Got event from the agent: %s", event)
            if event == USER_NOTIFIED:
                self.on_user_notified(**item[1])
            elif event == JOB_ACCEPTED:
                self.on_job_accepted(**item[1])
            elif event == JOB_REJECTED:
                self.on_job_rejected(**item[1])
            elif event == JOB_FINISHED:
                self.on_job_finished(**item[1])
            elif event == JOB_FAILED:
                self.on_job_failed(**item[1])
            elif event == AGENT_STOPPED:
                self.on_agent_stopped()

        except Queue.Empty:
            # ignored.
            pass

    def _terminate(self):
        _logger.info("Requested to terminate.")
        sys.exit(0)

    @abstractmethod
    def _run(self):
        """ Starts up the shell.
        """
        pass
