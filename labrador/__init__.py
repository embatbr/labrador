#! coding: utf-8

from bombril.logging import get_logger


class BaseObject(object):

    def __init__(self):
        self._logger = get_logger(__name__)

    @property
    def my_name(self):
        return '<{}.{}>'.format(self.__class__.__name__, id(self))
