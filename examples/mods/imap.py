# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import imaplib
import re
from ava.task import action


@action
def check_gmail(username, password):
    """Check GMail

    E.g.
        messages,unseen = imap.check_gmail('username@gmail.com','password')
    :param username:
    :param password:
    :return:
    """
    i = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        i.login(username, password)
        x, y = i.status('INBOX', '(MESSAGES UNSEEN)')
        messages = int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
        unseen = int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))
        return messages, unseen
    except:
        return False, 0
