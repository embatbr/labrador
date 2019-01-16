#! coding: utf-8

import os

from labrador.retrievers._base import Retriever
from labrador.retrievers.bigquery import BigQueryRetriever


def test_class(cls, *args, **kwargs):
    print('class:', cls)

    with cls(*args, **kwargs) as retriever:
        print('instance:', retriever)

        for rows in retriever.retrieve():
            print(type(rows))
            print(len(rows))
            print(rows)


if __name__ == '__main__':
    test_class(Retriever)
    print()
    test_class(BigQueryRetriever, **{
        'credentials': os.environ['BIGQUERY_CREDENTIALS'],
        'query_template': 'SELECT {columns} FROM `{project}.{dataset}.{table}` LIMIT {limit}',
        'query_args': {
            'columns': ', '.join(['spc_latin', 'spc_common']),
            'project': 'bigquery-public-data',
            'dataset': 'new_york',
            'table': 'tree_census_2015',
            'limit': 11
        },
        'fetch_size': 5
    })
