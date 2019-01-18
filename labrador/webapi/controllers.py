# -*- coding: utf-8 -*-

import falcon
import json

from labrador import BaseObject


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

        # self.retriever_executor = retriever_executor

    def _on_post(self, req, resp):
        payload = req.stream.read()
        try:
            payload = payload.decode('utf8')
            payload = json.loads(payload)

        except json.decoder.JSONDecodeError as err:
            self._logger.log_exception(err)
            resp.status = falcon.HTTP_400

#         steps = payload.get('steps')

#         status = None
#         try:
#             self.retriever_executor.submit_job(steps)
#             status = 'success'

#         except Exception as err:
#             logger.error(err)
#             status = 'failed'

#         resp.status = falcon.HTTP_200
#         resp.body = json.dumps({
#             'status': status
#         })
