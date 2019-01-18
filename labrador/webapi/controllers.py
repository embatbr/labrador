# -*- coding: utf-8 -*-

import falcon
import json

import labrador
from labrador.labrador import BaseObject


class Controller(BaseObject):

    def __init__(self):
        BaseObject.__init__(self)

    def on_get(self, req, resp):
        self._logger.info('Request {} received', str(req))

        self._on_get(req, resp)

        self._logger.info('Response {} sent', str(resp))
        # TODO log the body (it is broken)

    def on_post(self, req, resp):
        self._logger.info('Request {} received', str(req))

        self._on_post(req, resp)

        self._logger.info('Response {} sent', str(resp))


class HealthController(Controller):

    def __init__(self):
        Controller.__init__(self)

    def _on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'message': 'Healthy as a horse'
        })


class RetrieverController(Controller):

    def __init__(self):
        Controller.__init__(self)

    def _on_post(self, req, resp):
        payload = req.stream.read()
        try:
            payload = payload.decode('utf8')
            payload = json.loads(payload)

        except json.decoder.JSONDecodeError as err:
            self._logger.log_exception(err)
            resp.status = falcon.HTTP_400

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
