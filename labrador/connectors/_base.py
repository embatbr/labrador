#! coding: utf-8

"""This module contains base code. The classes, functions and other objects here
defined are not intended to be used outside of this library, althought that is
not any sort of "prohibition".
"""


class Connector(object):
    """The base connector class.
    """

    def __init__(self, retriever, sinker):
        self._retriever = retriever
        self._sinker = sinker

    def _convert(self, data):
        """This method must do simple conversions (for the sinkers). It is not
        intended to be a place to write processing code.
        """
        return data

    def connect(self):
        with self._sinker:
            with self._retriever:
                for data in self._retriever.retrieve():
                    converted_data = self._convert(data)
                    self._sinker.sink(converted_data)
