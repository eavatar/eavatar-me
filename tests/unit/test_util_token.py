# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from ava.util import crypto
from ava.util import token


class TestUtilToken(object):

    def test_can_encode_and_decode_token(self):

        alice_keys = crypto.generate_keypair()
        bob_keys = crypto.generate_keypair()

        #
        payload = {'iss': crypto.key_to_xid(alice_keys[0])}

        # Alice signed the payload to Bob
        encoded_token = token.encode(payload, alice_keys[1], bob_keys[0])

        print("ecnoded_token", encoded_token)
        decoded_payload = token.decode(encoded_token, bob_keys[1])

        assert 'iss' in decoded_payload
