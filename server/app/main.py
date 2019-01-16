# -*- coding: utf-8 -*-

import falcon
import logging
logging.basicConfig(level=logging.INFO)

from app import controllers
from app import executors
from app import retrievers


logger = logging.getLogger(__file__)


class RESTfulApplication(object):

    def __init__(self, logger, application, routes):
        self.logger = logger
        self.application = application
        self.routes = routes

    def expose(self):
        for (endpoint, controller) in self.routes.items():
            self.application.add_route(endpoint, controller)
            self.logger.info("Binding controller {} to route '{}'".format(controller, endpoint))

        self.logger.info('All routes exposed')


application = falcon.API()

retriever_executor = executors.RetrieverExecutor(retrievers.retrievers)

routes = {
    '/health': controllers.HealthController(),
    '/job': controllers.RetrieverController(retriever_executor)
}


restful_application = RESTfulApplication(logger, application, routes)
restful_application.expose()
