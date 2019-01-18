#! coding: utf-8

from google.cloud import bigquery
import hashlib
import os

from labrador.accredited import Accredited
from labrador.retrievers._base import Retriever


class BigQueryRetriever(Accredited, Retriever):

    def __init__(self, credentials, query, fetch_size=10*1000):
        Accredited.__init__(self, credentials)
        Retriever.__init__(self)

        self._query = query
        self._fetch_size = fetch_size

    def __enter__(self):
        self._connect()
        return Retriever.__enter__(self)

    def __exit__(self, _type, value, traceback):
        self._disconnect()
        Retriever.__exit__(self, _type, value, traceback)

    def _connect(self):
        Accredited._connect(self)

        m = hashlib.sha256()
        m.update('bigquery-credentials'.encode('utf8'))
        filename = m.hexdigest()
        filepath = '/tmp/{}.json'.format(filename)

        try:
            with open(filepath, 'w') as f:
                f.write(self._credentials)

            self._client = bigquery.Client.from_service_account_json(filepath)

        except Exception as e:
            raise e

        finally:
            self._post_connect()
            os.remove(filepath)

    def __retrieve_row(self):
        query_job = self._client.query(self._query)
        results = query_job.result()

        for row in results:
            yield dict(row)

    def retrieve(self):
        rows = list()

        for row in self.__retrieve_row():
            rows.append(row)

            if len(rows) == self._fetch_size:
                yield rows
                rows = list()

        if len(rows) > 0:
            yield rows