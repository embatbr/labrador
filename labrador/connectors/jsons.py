#! coding: utf-8

import json

from labrador.connectors._base import Connector


class JSONListConnector(Connector):

    def __init__(self, retriever, sinker):
        Connector.__init__(self, retriever, sinker)

    def _convert(self, data):
        self._logger.info('Converting {} objects', len(data))

        converted_data = '\n'.join([json.dumps(obj) for obj in data])
        return Connector._convert(self, converted_data)
