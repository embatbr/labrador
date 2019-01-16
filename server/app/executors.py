# -*- coding: utf-8 -*-

import json
import logging
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__file__)


class RetrieverExecutor(object):

    def __init__(self, retrievers):
        self.retrievers = retrievers

    def submit_job(self, steps):
        for step in steps:
            action = step['action']

            if action == 'retrieve':
                retriever_type = step['retriever_type']
                retriever_args = step.get('retriever_args', dict())

                retriever = self.retrievers[retriever_type](**retriever_args)
                result = retriever.retrieve()

                filename = step['filename']

                with open(filename, 'w') as f:
                    logger.info('fetching rows')

                    while True:
                        row = next(result, None)
                        if row is None:
                            break

                        f.write('{}\n'.format(json.dumps(row, ensure_ascii=False)))

                    logger.info('all rows fetched')
