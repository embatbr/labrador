# -*- coding: utf-8 -*-

import falcon
import json
import logging
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__file__)


class HealthController(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'message': 'Healthy as a horse'
        })

class RetrieverController(object):

    def __init__(self, retriever_executor):
        self.retriever_executor = retriever_executor

    def on_post(self, req, resp):
        payload = req.stream.read()
        try:
            payload = payload.decode('utf8')
            payload = json.loads(payload)
        except json.decoder.JSONDecodeError as err:
            logger.error(str(err))
            resp.status = falcon.HTTP_400

        steps = payload.get('steps')

        status = None
        try:
            self.retriever_executor.submit_job(steps)
            status = 'success'

        except Exception as err:
            logger.error(err)
            status = 'failed'

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'status': status
        })
