# -*- coding: utf-8 -*-

import labrador
from labrador.labrador import BaseObject


class Executor(BaseObject):

    def __init__(self):
        BaseObject.__init__(self)

    def execute(self, payload):
        moduler_connectors = getattr(labrador, 'connectors')
        moduler_retrievers = getattr(labrador, 'retrievers')
        moduler_sinkers = getattr(labrador, 'sinkers')

        connector_cls = getattr(moduler_connectors, payload['connector']).INTERFACE
        retriever_cls = getattr(moduler_retrievers, payload['retriever']).INTERFACE
        sinker_cls = getattr(moduler_sinkers, payload['sinker']).INTERFACE

        parameters = payload['parameters']

        retriever = retriever_cls(**parameters['retriever'])
        sinker = sinker_cls(**parameters['sinker'])
        connector = connector_cls(retriever, sinker)
        connector.connect()
