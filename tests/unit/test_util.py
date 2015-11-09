# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
from ava.util import time_uuid, base_path, defines


class TestTimeUUID(object):

    def test_uuids_should_be_in_alaphabetical_order(self):
        old = time_uuid.oid()
        for i in range(100):
            t = time_uuid.oid()
            assert t > old
            old = t


def test_base_path_should_contain_pod_folder():

    basedir = base_path()
    source_pod_folder = os.path.join(basedir, defines.POD_FOLDER_NAME)
    assert os.path.exists(source_pod_folder)
    assert os.path.isdir(source_pod_folder)
