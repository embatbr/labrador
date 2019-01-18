#! coding: utf-8

"""Module with a single class to try to implement some security.
"""

import os
from bombril.cryptography.rsa import decrypt_chunks


class Secured(object):

    def __init__(self, credentials):
        self._credentials = credentials

    def _connect(self):
        # TODO extract to mother class "Secure"
        private_key_pem = os.environ['PRIVATE_KEY_PEM']
        self._credentials = decrypt_chunks(self._credentials, private_key_pem)
        del private_key_pem

    def _post_connect(self):
        del self._credentials

    def _disconnect(self):
        del self._client
