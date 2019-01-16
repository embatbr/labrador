# -*- coding: utf-8 -*-

import base64
import json
import logging
logging.basicConfig(level=logging.INFO)
import os

from google.cloud import bigquery


logger = logging.getLogger(__file__)


class Retriever(object):

    def __init__(self):
        pass


class BigQueryRetriever(Retriever):

    def __init__(self, query_template, query_args=dict()):
        super(BigQueryRetriever, self).__init__()

        self.query_template = query_template
        self.query_args = query_args

        credentials = os.environ.get('BIGQUERY_CREDENTIALS_BASE64')

        with open('bigquery-credentials.json', 'w') as f:
            f.write(base64.b64decode(credentials).decode('utf8'))

        self.client = bigquery.Client.from_service_account_json('bigquery-credentials.json')
        os.remove('bigquery-credentials.json')

    def retrieve(self):
        query = self.query_template.format(**self.query_args)

        query_job = self.client.query(query)
        results = query_job.result()

        for row in results:
            yield dict(row)


retrievers = {
    'bigquery': BigQueryRetriever
}
