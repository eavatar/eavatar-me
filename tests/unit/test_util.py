# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import time
from ava.util import time_uuid


class TestTimeUUID(object):

    def test_time_uuid_order(self):
        old = time_uuid.oid()
        for i in range(1000):
            time.sleep(0.01)
            t = time_uuid.oid()
            print(t)
            assert t > old
            old = t