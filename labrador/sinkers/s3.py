#! coding: utf-8

import boto3
import json

from labrador.secured import Secured
from labrador.sinkers._base import Sinker


class S3Sinker(Secured, Sinker):

    def __init__(self, credentials):
        Secured.__init__(self, credentials)
        Sinker.__init__(self)

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
            raise e

        finally:
            self._post_connect()

    def sink(self, data, place):
        obj = self._client.Object(
            place['bucket_name'],
            '{}/{}'.format(place['prefix'], place['filename'])
        )

        obj.put(Body=data)
