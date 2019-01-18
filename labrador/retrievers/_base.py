#! coding: utf-8

"""This module contains base code. The classes, functions and other objects here
defined are not intended to be used outside of this library, althought that is
not any sort of "prohibition".
"""


class Retriever(object):
    """The base retriever class.
    """

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def retrieve(self):
        yield list()
