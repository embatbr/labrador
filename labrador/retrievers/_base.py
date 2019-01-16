#! coding: utf-8


class Retriever(object):

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def retrieve(self):
        yield list()
