#! coding: utf-8

import json
import os
import sys
import time

from labrador.connectors.jsonlist import JSONListConnector
from labrador.retrievers.bigquery import BigQueryRetriever
from labrador.sinkers.s3 import S3Sinker


CREDENTIALS_FILEPATH = sys.argv[1].strip()
BUCKET_NAME = sys.argv[2].strip()

BIGQUERY_CREDENTIALS = open('{}/bigquery.encrypted'.format(CREDENTIALS_FILEPATH)).read()
S3_CREDENTIALS = open('{}/s3.encrypted'.format(CREDENTIALS_FILEPATH)).read()


if __name__ == '__main__':
    retriever = BigQueryRetriever(
        credentials=BIGQUERY_CREDENTIALS,
        query='SELECT {columns} FROM `{project}.{dataset}.{table}` LIMIT {limit}'.format(**{
            'columns': ', '.join(['spc_latin', 'spc_common']),
            'project': 'bigquery-public-data',
            'dataset': 'new_york',
            'table': 'tree_census_2015',
            'limit': 100*1000
        }),
        fetch_size=10*1000
    )

    sinker = S3Sinker(
        credentials=S3_CREDENTIALS,
        bucket_name=BUCKET_NAME,
        key='dev/labrador/test.jsonl'
    )

    connector = JSONListConnector(retriever, sinker)
    connector.connect()
