# -*- coding: utf-8 -*-

for i in ava.schedule.counts(1).every(3).seconds:
    ava.do('user.notify', msg="This is a test notice %d" % i, title="Message %d" % i)