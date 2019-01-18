#! coding: utf-8

"""Module with a single class to try to implement some security.
"""

from bombril.cryptography.rsa import decrypt_chunks
import os

from labrador import BaseObject


class Secured(BaseObject):

    def __init__(self, credentials):
        BaseObject.__init__(self)
        self._credentials = credentials

    def _connect(self):
        self._logger.info('Connecting {}', self.my_name)

        private_key_pem = os.environ['PRIVATE_KEY_PEM']
        self._credentials = decrypt_chunks(self._credentials, private_key_pem)
        del private_key_pem

    def _post_connect(self):
        del self._credentials

        self._logger.info('{} connected', self.my_name)

    def _disconnect(self):
        del self._client

        self._logger.info('{} disconnected', self.my_name)
