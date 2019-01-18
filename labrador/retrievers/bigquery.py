#! coding: utf-8

from google.cloud import bigquery
import hashlib
import os

from labrador.labrador import Secured
from labrador.retrievers.retriever import Retriever


class BigQueryRetriever(Secured, Retriever):

    def __init__(self, credentials, query, fetch_size=10*1000):
        Secured.__init__(self, credentials)
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
        Secured._connect(self)

        m = hashlib.sha256()
        m.update('bigquery-credentials'.encode('utf8'))
        filename = m.hexdigest()
        filepath = '/tmp/{}.json'.format(filename)

        try:
            with open(filepath, 'w') as f:
                self._logger.info('Writing credentials to file {}', filepath)
                f.write(self._credentials)

            self._client = bigquery.Client.from_service_account_json(filepath)
            self._logger.info('Client {} created', self._client)

        except Exception as err:
            self._logger.log_exception(err)
            raise err

        finally:
            self._post_connect()
            if os.path.isfile(filepath):
                self._logger.info('Removing file {}', filepath)
                os.remove(filepath)

    def _retrieve_row(self):
        query_job = self._client.query(self._query)
        results = query_job.result()

        for row in results:
            yield dict(row)

    def retrieve(self):
        rows = list()

        for row in self._retrieve_row():
            rows.append(row)

            row_amount = len(rows)
            if row_amount == self._fetch_size:
                self._logger.info('Retrieving {} rows', row_amount)
                yield rows
                rows = list()

        row_amount = len(rows)
        if row_amount > 0:
            self._logger.info('Retrieving {} rows', row_amount)
            yield rows


INTERFACE = BigQueryRetriever
