#! coding: utf-8

import requests as r
import sys


BASE_URL = 'http://localhost:9001'

CREDENTIALS_FILEPATH = sys.argv[1].strip()
BUCKET_NAME = sys.argv[2].strip()
TEST_ID = sys.argv[3].strip()

BIGQUERY_CREDENTIALS = open('{}/bigquery.encrypted'.format(CREDENTIALS_FILEPATH)).read()
S3_CREDENTIALS = open('{}/s3.encrypted'.format(CREDENTIALS_FILEPATH)).read()


resp = r.get('{}/health'.format(BASE_URL))
assert resp.status_code == 200
assert resp.json() == {
    'message': 'Healthy as a horse'
}

resp = r.post('{}/retrieve'.format(BASE_URL), json={
    "retriever": "bigquery",
    "sinker": "s3",
    "connector": "jsonlist",
    "parameters": {
        "retriever": {
            "credentials": BIGQUERY_CREDENTIALS,
            "query": "SELECT {columns} FROM `{project}.{dataset}.{table}` LIMIT {limit}".format(**{
                "columns": ", ".join(["spc_latin", "spc_common"]),
                "project": "bigquery-public-data",
                "dataset": "new_york",
                "table": "tree_census_2015",
                "limit": 100*1000
            }),
            "fetch_size": 10*1000
        },
        "sinker": {
            "credentials": S3_CREDENTIALS,
            "bucket_name": BUCKET_NAME,
            "key": "dev/labrador/test_{}.jsonl".format(TEST_ID)
        }
    }
})
