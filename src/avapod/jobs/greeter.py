# -*- coding: utf-8 -*-

for i in ava.schedule.counts(3).every(3).seconds:
    ava.do('user.notify', message="This is a test notice %d" % i, title="Message %d" % i)