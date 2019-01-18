#! coding: utf-8

import json
import os
import sys
import time

from labrador.retrievers._base import Retriever
from labrador.retrievers.bigquery import BigQueryRetriever

from labrador.sinkers._base import Sinker
from labrador.sinkers.s3 import S3Sinker


FILEPATH = sys.argv[1].strip()
BUCKET_NAME = sys.argv[2].strip()

BIGQUERY_CREDENTIALS = open('{}/bigquery.encrypted'.format(FILEPATH)).read()
S3_CREDENTIALS = open('{}/s3.encrypted'.format(FILEPATH)).read()


def test_class(cls_dict, cls_kwargs=dict()):
    with cls_dict['sinker'](**cls_kwargs.get('sinker', dict())) as sinker:
        print('sinker:', sinker)

        with cls_dict['retriever'](**cls_kwargs.get('retriever', dict())) as retriever:
            print('retriever:', retriever)

            for rows in retriever.retrieve():
                rows = '\n'.join([json.dumps(row) for row in rows])

                sinker.sink(rows, {
                    'bucket_name': BUCKET_NAME,
                    'prefix': 'dev/labrador',
                    'filename': 'test-{}.jsonl'.format(time.time())
                })


if __name__ == '__main__':
    test_class(
        {
            'retriever': Retriever,
            'sinker': Sinker
        }
    )

    print()

    test_class(
        {
            'retriever': BigQueryRetriever,
            'sinker': S3Sinker
        },
        {
            'retriever': {
                'credentials': BIGQUERY_CREDENTIALS,
                'query': 'SELECT {columns} FROM `{project}.{dataset}.{table}` LIMIT {limit}'.format(**{
                    'columns': ', '.join(['spc_latin', 'spc_common']),
                    'project': 'bigquery-public-data',
                    'dataset': 'new_york',
                    'table': 'tree_census_2015',
                    'limit': 14
                }),
                'fetch_size': 5
            },
            'sinker': {
                'credentials': S3_CREDENTIALS,
            }
        }
    )
