# -*- coding: utf-8 -*-

import falcon
import json
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

    def __init__(self, executor):
        Controller.__init__(self)

        self._executor = executor

    def _on_post(self, req, resp):
        try:
            payload = req.stream.read()
            payload = payload.decode('utf8')
            payload = json.loads(payload)

            self._executor.execute(payload)

        except json.decoder.JSONDecodeError as err:
            self._logger.log_exception(err)
            resp.status = falcon.HTTP_400
