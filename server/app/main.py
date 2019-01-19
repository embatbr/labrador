# -*- coding: utf-8 -*-

import falcon
from labrador.labrador import BaseObject

from app import controllers
from app import executors


class RESTfulApplication(BaseObject):

    def __init__(self, application, routes):
        BaseObject.__init__(self)

        self._application = application
        self._routes = routes

    def expose(self):
        for (endpoint, controller) in self._routes.items():
            self._application.add_route(endpoint, controller)
            self._logger.info("Binding controller {} to endpoint '{}'".format(controller, endpoint))

        self._logger.info('All endpoints exposed')


application = falcon.API()

executor = executors.Executor()

routes = {
    '/health': controllers.HealthController(),
    '/retrieve': controllers.RetrieverController(executor)
}


restful_application = RESTfulApplication(application, routes)
restful_application.expose()
