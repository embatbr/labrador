#! coding: utf-8

"""This module contains base code. The classes, functions and other objects here
defined are not intended to be used outside of this library, althought that is
not any sort of "prohibition".
"""

from bombril.logging import get_logger


class Retriever(object):
    """The base retriever class.
    """

    def __init__(self):
        self._logger = get_logger(__name__)

    def __enter__(self):
        self._logger.info('Returning {}', self.my_name)
        return self

    def __exit__(self, _type, value, traceback):
        pass

    def retrieve(self):
        yield list()
