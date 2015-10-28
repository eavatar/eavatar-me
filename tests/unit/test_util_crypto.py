# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import unittest
import libnacl.public
import libnacl.secret
import libnacl.utils
import pyscrypt
import base58
import binascii
from ava.util import crypto


class TestCrypto(unittest.TestCase):

    def test_generate_keypair(self):
        bob = libnacl.public.SecretKey()
        assert bob is not None

        self.assertEqual(len(bob.sk), 32)
        sk = base58.b58encode(bob.sk)
        pk = base58.b58encode(bob.pk)
        xid = crypto.key_to_xid(bob.pk)

        print("Public key: ", pk, ", len: ", len(pk))
        print("Secret key: ", sk, ", len: ", len(sk))
        print("XID: ", xid, ", len: ", len(xid))

    def test_public_key_encryption(self):
        msg = b'You\'ve got two empty halves of coconut and you\'re bangin\' \'em together.'
        bob = libnacl.public.SecretKey()
        alice = libnacl.public.SecretKey()
        bob_box = libnacl.public.Box(bob.sk, alice.pk)
        alice_box = libnacl.public.Box(alice.sk, bob.pk)
        bob_ctxt = bob_box.encrypt(msg)
        bclear = alice_box.decrypt(bob_ctxt)
        alice_ctxt = alice_box.encrypt(msg)
        aclear = alice_box.decrypt(alice_ctxt)

        self.assertEqual(bclear, aclear)
        self.assertEqual(bclear, msg)

    def test_public_key_encryption_util(self):
        alice = crypto.generate_keypair()
        bob = crypto.generate_keypair()

        ciphertext = crypto.public_key_encrypt(alice[1], bob[0], "hello")
        plaintext = crypto.public_key_decrypt(bob[1], alice[0], ciphertext)
        self.assertEqual("hello", plaintext)

    def test_secret_key_encryption(self):
        msg = b'But then of course African swallows are not migratory.'
        # Create a SecretBox object, if not passed in the secret key is
        # Generated purely from random data
        box = libnacl.secret.SecretBox()
        # Messages can now be safely encrypted
        ctxt = box.encrypt(msg)
        # An addition box can be created from the original box secret key
        box2 = libnacl.secret.SecretBox(box.sk)
        # Messages can now be easily encrypted and decrypted
        clear1 = box.decrypt(ctxt)
        clear2 = box2.decrypt(ctxt)
        ctxt2 = box2.encrypt(msg)
        clear3 = box.decrypt(ctxt2)

        self.assertEqual(clear1, clear2)
        self.assertEqual(clear2, clear3)
        self.assertEqual(msg, clear1)

    def test_nonce_generation(self):

        prev_nonce = libnacl.utils.rand_nonce()
        for i in xrange(100):
            nonce = libnacl.utils.rand_nonce()
            self.assertNotEqual(prev_nonce, nonce)
            prev_nonce = nonce

    def test_demo_user_keys(self):
        sk_base58 = b"29oiwbqkhLGBuX5teL5d2vsiJ3EXk3dpyBiPwA7W9DJG"
        sk_decoded = base58.b58decode(sk_base58)
        hash = pyscrypt.hash(password=b"demouser",
                             salt=b"demouser",
                             N=1024,
                             r=1,
                             p=1,
                             dkLen=32)

        sk = base58.b58encode(hash)
        hex_sk = binascii.b2a_hex(hash)
        print('Secret Key:', sk, 'length: ', len(sk))
        self.assertEqual(sk_base58, sk)
        self.assertEqual(sk_decoded, hash)

        #print(sk)
        keypair = libnacl.public.SecretKey(hash)

        # 2ipFYsqXnrw4Mt2RUWzEQntAH1FEFB8R52rAT3eExn9S
        pk_base58 = base58.b58encode(keypair.pk)
        pk_decoded = base58.b58decode(pk_base58)

        self.assertEqual(pk_decoded, keypair.pk)
        print('Public Key:', pk_base58, 'length: ', len(pk_base58))

        print("XID: ", crypto.key_to_xid(keypair.pk))

    def test_calc_shared_key_via_two_key_pairs(self):
        bob = libnacl.public.SecretKey()
        alice = libnacl.public.SecretKey()
        alice_key = libnacl.crypto_box_beforenm(bob.pk, alice.sk)
        bob_key = libnacl.crypto_box_beforenm(alice.pk, bob.sk)
        #print(base58.b58encode(bob_key))
        self.assertEqual(bob_key, alice_key)

    def test_key_to_fingerprint(self):
        bob = libnacl.public.SecretKey()
        assert bob is not None

        pk = bob.pk

        fp = crypto.key_to_fingerprint(pk)
        print("FP: ", fp, ", len: ", len(fp))

    def test_convert_key_to_xid_back_and_forth(self):
        keypair = libnacl.public.SecretKey()
        xid = crypto.key_to_xid(keypair.pk)
        print(xid)
        self.assertTrue(crypto.validate_xid(xid))
        pk = crypto.xid_to_key(xid)
        self.assertEqual(keypair.pk, pk)

    def test_convert_key_to_string_back_and_forth(self):
        keypair = libnacl.public.SecretKey()
        pk_str = crypto.key_to_string(keypair.pk)
        # print(pk_str)
        self.assertTrue(crypto.validate_key_string(pk_str))
        pk = crypto.string_to_key(pk_str)
        self.assertEqual(keypair.pk, pk)

    def test_convert_secret_to_string_back_and_forth(self):
        keypair = libnacl.public.SecretKey()
        sk_str = crypto.secret_to_string(keypair.sk)
        # print(sk_str)
        self.assertTrue(crypto.validate_secret_string(sk_str))
        sk = crypto.string_to_secret(sk_str)
        self.assertEqual(keypair.sk, sk)