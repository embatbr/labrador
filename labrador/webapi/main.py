# -*- coding: utf-8 -*-


import falcon

from labrador.labrador import BaseObject
from labrador.webapi import controllers


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

routes = {
    '/health': controllers.HealthController(),
    '/retrieve': controllers.RetrieverController()
}


restful_application = RESTfulApplication(application, routes)
restful_application.expose()
