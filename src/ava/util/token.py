# -*- coding: utf-8 -*-
"""
The module provides functions for access token manipulation.
"""
from __future__ import absolute_import, print_function, unicode_literals

import json
import binascii
import logging
from hashlib import sha256
from calendar import timegm
from collections import Mapping
from datetime import datetime, timedelta

from .crypto import (
    string_to_key,
    string_to_secret,
    xid_to_key,
    public_key_encrypt,
    public_key_decrypt,
    SECRET_PREFIX,
    KEY_PREFIX,
)

from .codecs import base64url_decode, base64url_encode
from .compat import string_types

logger = logging.getLogger(__name__)


def timedelta_total_seconds(delta):
    try:
        delta.total_seconds
    except AttributeError:
        # On Python 2.6, timedelta instances do not have
        # a .total_seconds() method.
        total_seconds = delta.days * 24 * 60 * 60 + delta.seconds
    else:
        total_seconds = delta.total_seconds()

    return total_seconds


class DecodeError(ValueError):
    pass


class ExpiredSignatureError(ValueError):
    pass


def sign(msg, issuer_sk, audience_pk):
    if issuer_sk.startswith(SECRET_PREFIX):
        issuer_sk = string_to_secret(issuer_sk)
    if audience_pk.startswith(KEY_PREFIX):
        audience_pk = string_to_key(audience_pk)

    h = sha256(msg).digest()
    sig = public_key_encrypt(issuer_sk, audience_pk, h)
    return sig


def _verify(msg, issuer_pk, audience_sk, sig):
    if isinstance(audience_sk, string_types):
        logger.debug("audience_sk: %s", audience_sk)
        audience_sk = audience_sk

    hashval = sha256(msg).digest()
    verifyval = public_key_decrypt(audience_sk, issuer_pk, sig)
    return hashval == verifyval


def encode(payload, issuer_sk, audience_pk, headers=None):
    segments = []
    header = {'typ': 'JWT', 'alg': 'EA256'}
    if headers:
        header.update(headers)

    json_header = json.dumps(
        header,
        separators=(',', ':')
    ).encode('utf-8')

    segments.append(base64url_encode(json_header))

    # Payload
    for time_claim in ['exp', 'iat', 'nbf']:
        # Convert datetime to a intDate value in known time-format claims
        if isinstance(payload.get(time_claim), datetime):
            payload[time_claim] = timegm(payload[time_claim].utctimetuple())

    json_payload = json.dumps(
        payload,
        separators=(',', ':')
    ).encode('utf-8')

    segments.append(base64url_encode(json_payload))

    # Segments
    signing_input = b'.'.join(segments)
    signature = sign(signing_input, issuer_sk, audience_pk)

    segments.append(base64url_encode(signature))

    return b'.'.join(segments)


def decode(tok, audience_sk, verify=True, **kwargs):
    payload, signing_input, header, signature = load(tok)

    if audience_sk.startswith(SECRET_PREFIX):
        audience_sk = string_to_secret(audience_sk)

    if verify:
        verify_signature(payload, signing_input, header, signature,
                         audience_sk, **kwargs)

    return payload


def verify_signature(payload, signing_input, header, signature, audience_sk,
                     verify_expiration=True, leeway=0, audience=None):

    if isinstance(leeway, timedelta):
        leeway = timedelta_total_seconds(leeway)

    issuer_pk = payload.get('iss')
    if issuer_pk is None:
        issuer_pk = payload.get('sub')

    if issuer_pk is None:
        raise DecodeError("Issuer or subject not found.")

    issuer_pk = xid_to_key(issuer_pk)

    if not _verify(signing_input, issuer_pk, audience_sk, signature):
        raise DecodeError('Signature verification failed')

    if 'nbf' in payload and verify_expiration:
        utc_timestamp = timegm(datetime.utcnow().utctimetuple())

        if payload['nbf'] > (utc_timestamp + leeway):
            raise ExpiredSignatureError('Signature not yet valid')

    if 'exp' in payload and verify_expiration:
        utc_timestamp = timegm(datetime.utcnow().utctimetuple())

        if payload['exp'] < (utc_timestamp - leeway):
            raise ExpiredSignatureError('Signature has expired')


def load(tok):
    # if isinstance(tok, text_type):
    #     tok = tok.encode('utf-8')

    try:
        signing_input, crypto_segment = tok.rsplit(b'.', 1)
        header_segment, payload_segment = signing_input.split(b'.', 1)
    except ValueError:
        raise DecodeError('Not enough segments')

    try:
        header_data = base64url_decode(header_segment)
    except (TypeError, binascii.Error):
        raise DecodeError('Invalid header padding')

    try:
        header = json.loads(header_data)
    except ValueError as e:
        raise DecodeError('Invalid header string: %s' % e)

    if not isinstance(header, Mapping):
        raise DecodeError('Invalid header string: must be a json object')

    try:
        payload_data = base64url_decode(payload_segment)
    except (TypeError, binascii.Error):
        raise DecodeError('Invalid payload padding')

    try:
        payload = json.loads(payload_data)
    except ValueError as e:
        raise DecodeError('Invalid payload string: %s' % e)

    if not isinstance(payload, Mapping):
        raise DecodeError('Invalid payload string: must be a json object')

    try:
        signature = base64url_decode(crypto_segment)
    except (TypeError, binascii.Error):
        raise DecodeError('Invalid crypto padding')

    return payload, signing_input, header, signature
