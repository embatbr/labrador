#! coding: utf-8

import hashlib
import json
import os

from google.cloud import bigquery
from labrador.retrievers._base import Retriever


def _get_bigquery_client(filepath, credentials):
    # TODO add decryption
    # credentials = base64.b64decode(credentials).decode('utf8')

    try:
        with open(filepath, 'w') as f:
            f.write(credentials)

        client = bigquery.Client.from_service_account_json(filepath)
    except Exception as e:
        raise e
    finally:
        os.remove(filepath)

    return client


class BigQueryRetriever(Retriever):

    def __init__(self, credentials, query_template, query_args, fetch_size=10*1000):
        super(BigQueryRetriever, self).__init__()

        self._credentials = credentials

        self.query_template = query_template
        self.query_args = query_args
        self.fetch_size = fetch_size

    def __enter__(self):
        m = hashlib.sha256()
        m.update('bigquery-credentials'.encode('utf8'))
        filename = m.hexdigest()
        filepath = '/tmp/{}.json'.format(filename)

        self.client = _get_bigquery_client(filepath, self._credentials)
        del self._credentials

        return super(BigQueryRetriever, self).__enter__()

    def _retrieve_row(self):
        query = self.query_template.format(**self.query_args)

        query_job = self.client.query(query)
        results = query_job.result()

        for row in results:
            yield dict(row)

    def retrieve(self):
        rows = list()

        for row in self._retrieve_row():
            rows.append(row)

            if len(rows) == self.fetch_size:
                yield rows
                rows = list()

        if rows:
            yield rows