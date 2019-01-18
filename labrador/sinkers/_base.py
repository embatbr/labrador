#! coding: utf-8

"""This module contains base code. The classes, functions and other objects here
defined are not intended to be used outside of this library, althought that is
not any sort of "prohibition".
"""


class Sinker(object):
    """The base sinker class.
    """

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        pass

    def sink(self, data, place):
        pass
