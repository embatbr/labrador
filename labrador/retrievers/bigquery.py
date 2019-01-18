#! coding: utf-8

from bombril.cryptography.rsa import decrypt_chunks
from google.cloud import bigquery
import hashlib
import json
import os

from labrador.retrievers._base import Retriever


class BigQueryRetriever(Retriever):

    def __init__(self, credentials, query, fetch_size=10*1000):
        super(BigQueryRetriever, self).__init__()

        self.__credentials = credentials
        self._query = query
        self._fetch_size = fetch_size

    def __enter__(self):
        self.__connect()
        return super(BigQueryRetriever, self).__enter__()

    def __exit__(self, _type, value, traceback):
        self.__disconnect()
        super(BigQueryRetriever, self).__exit__(_type, value, traceback)

    def __connect(self):
        # TODO extract to mother class "Secure"
        private_key_pem = os.environ['PRIVATE_KEY_PEM']
        self.__credentials = decrypt_chunks(self.__credentials, private_key_pem)
        del private_key_pem

        m = hashlib.sha256()
        m.update('bigquery-credentials'.encode('utf8'))
        filename = m.hexdigest()
        filepath = '/tmp/{}.json'.format(filename)

        try:
            with open(filepath, 'w') as f:
                f.write(self.__credentials)
            del self.__credentials

            self._client = bigquery.Client.from_service_account_json(filepath)

        except Exception as e:
            raise e

        finally:
            os.remove(filepath)

    def __disconnect(self):
        # TODO extract to mother class "Secure"
        del self._client

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