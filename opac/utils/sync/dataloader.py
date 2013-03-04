import pymongo

from django.conf import settings

from catalog import mongomodels


class Marreta(object):

    def __init__(self, mongoconn_lib=mongomodels.MongoConnector,
                       pymongo_lib=pymongo,
                       settings=settings):

        mongo_uri = getattr(settings, 'MONGO_URI', None)

        if not mongo_uri:
            raise ValueError('missing config to mongodb')

        self._mongoconn = mongoconn_lib(mongodb_driver=pymongo_lib,
                                        mongo_uri=mongo_uri)

    def rebuild_collection(self, collection, new_data):
        """
        Drops the collection ``collection`` and rebuild it
        using ``new_data``.

        ``collection`` is a string of the collection name

        ``new_data`` is an iterable containing the data to
        be loaded after the collection is recreated.
        """
        self._mongoconn.db.drop_collection(collection)

        col = self._mongoconn.db[collection]
        mongomodels.ensure_all_indexes()

        for data in new_data:
            col.insert(data, w=1)

        return None

    def update_collection(self, collection, new_data):
        col = self._mongoconn.db[collection]

        for data in new_data:
            col.update({'id': data['id']}, data, w=1, upsert=True)

        return None
