# -*- coding: utf-8 -*-


import falcon

from labrador import BaseObject
from labrador.webapi import controllers
# import executors


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

# retriever_executor = executors.RetrieverExecutor(retrievers.retrievers)

routes = {
    '/health': controllers.HealthController(),
    '/retrieve': controllers.RetrieverController()
    # '/retrieve': controllers.RetrieverController(retriever_executor)
}


restful_application = RESTfulApplication(application, routes)
restful_application.expose()
