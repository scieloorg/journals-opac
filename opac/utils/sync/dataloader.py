import pymongo

from django.conf import settings

from catalog.mongomodels import MongoConnector


class Marreta(object):

    def __init__(self, mongoconn_lib=MongoConnector,
                       pymongo_lib=pymongo,
                       settings=settings):

        mongo_uri = getattr(settings, 'MONGO_URI', None)

        if not mongo_uri:
            raise ValueError('missing config to mongodb')

        self._mongoconn = mongoconn_lib(mongodb_driver=pymongo_lib,
                                        mongo_uri=mongo_uri)
