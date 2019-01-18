#! coding: utf-8

from bombril.cryptography.rsa import decrypt_chunks
import boto3
import json
import os

from labrador.sinkers._base import Sinker


class S3Sinker(Sinker):

    def __init__(self, credentials):
        super(S3Sinker, self).__init__()

        self.__credentials = credentials

    def __enter__(self):
        self.__connect()
        return super(S3Sinker, self).__enter__()

    def __exit__(self, _type, value, traceback):
        self.__disconnect()
        super(S3Sinker, self).__exit__(_type, value, traceback)

    def __connect(self):
        # TODO extract to mother class "Secure"
        private_key_pem = os.environ['PRIVATE_KEY_PEM']
        self.__credentials = decrypt_chunks(self.__credentials, private_key_pem)
        del private_key_pem

        self.__credentials = json.loads(self.__credentials)

        try:
            session = boto3.session.Session(**self.__credentials)
            del self.__credentials
            self._client = session.resource('s3')

        except Exception as e:
            raise e

    def __disconnect(self):
        # TODO extract to mother class "Secure"
        del self._client

    def sink(self, data, place):
        obj = self._client.Object(
            place['bucket_name'],
            '{}/{}'.format(place['prefix'], place['filename'])
        )

        obj.put(Body=data)
