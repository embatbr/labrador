#! coding: utf-8

"""Module with a single class to try to implement some security.
"""

from bombril.cryptography.rsa import decrypt_chunks
from bombril.logging import get_logger
import os


class Secured(object):

    def __init__(self, credentials):
        self._credentials = credentials

        self._secure_logger = get_logger(__name__)

    def _connect(self):
        self._secure_logger.info('Connecting {}', self.my_name)

        private_key_pem = os.environ['PRIVATE_KEY_PEM']
        self._credentials = decrypt_chunks(self._credentials, private_key_pem)
        del private_key_pem

    def _post_connect(self):
        del self._credentials

        self._secure_logger.info('{} connected', self.my_name)

    def _disconnect(self):
        del self._client

        self._secure_logger.info('{} disconnected', self.my_name)

    @property
    def my_name(self):
        return '<{}.{}>'.format(self.__class__.__name__, id(self))
