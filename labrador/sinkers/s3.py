#! coding: utf-8

import boto3
import json

from labrador.secured import Secured
from labrador.sinkers._base import Sinker


class S3Sinker(Secured, Sinker):

    __PARTITION_DIGITS = 10

    def __init__(self, credentials, bucket_name, key):
        Secured.__init__(self, credentials)
        Sinker.__init__(self)

        self._bucket_name = bucket_name
        self._key = key
        self._part = 0

    def __enter__(self):
        self._connect()
        return Sinker.__enter__(self)

    def __exit__(self, _type, value, traceback):
        self._disconnect()
        Sinker.__exit__(self, _type, value, traceback)

    def _connect(self):
        Secured._connect(self)

        self._credentials = json.loads(self._credentials)

        try:
            session = boto3.session.Session(**self._credentials)
            self._client = session.resource('s3')

        except Exception as e:
            self._logger.error('{}: "{}"', e.__class__.__name__, str(e))
            raise e

        finally:
            self._post_connect()

    def sink(self, data):
        part_zfilled = str(self._part).zfill(S3Sinker.__PARTITION_DIGITS)
        key = '{}/part_{}'.format(self._key, part_zfilled)
        self._part = self._part + 1

        obj = self._client.Object(self._bucket_name, key)
        obj.put(Body=data)
