# coding: utf-8
import logging
import time
import itertools

from django.conf import settings
import slumber
import requests


logger = logging.getLogger(__name__)
ITEMS_PER_REQUEST = 50


class ResourceUnavailableError(Exception):
    def __init__(self, *args, **kwargs):
        super(ResourceUnavailableError, self).__init__(*args, **kwargs)


class SciELOManagerAPI(object):
    """
    Responsible for collecting data from SciELO Manager's RESTful
    interface, and making them available as Python datastructures.
    """

    def __init__(self,
                 slumber_lib=slumber,
                 settings=settings):

        self._resource_url = getattr(settings, 'SCIELOMANAGER_API_URI', None)
        self._api_key = getattr(settings, 'SCIELOMANAGER_API_KEY', None)
        self._username = getattr(settings, 'SCIELOMANAGER_API_USERNAME', None)

        if not self._resource_url or not self._api_key or not self._username:
            raise ValueError('missing config to manager api')

        self._slumber_lib = slumber_lib
        self._api = self._slumber_lib.API(self._resource_url)

    def fetch_data(self, endpoint,
                         resource_id=None,
                         **kwargs):
        """
        Fetches the specified resource from the SciELO Manager API.
        """
        err_count = 0

        if all([self._username, self._api_key]):
            kwargs['username'] = self._username
            kwargs['api_key'] = self._api_key

        resource = getattr(self._api, endpoint)

        if resource_id:
            resource = resource(resource_id)

        while True:
            try:
                return resource.get(**kwargs)
            except requests.exceptions.ConnectionError as exc:
                if err_count < 10:
                    wait_secs = err_count * 5
                    logger.info('Connection failed. Waiting %ss to retry.' % wait_secs)
                    time.sleep(wait_secs)
                    err_count += 1
                    continue
                else:
                    logger.error('Unable to connect to resource (%s).' % exc)
                    raise ResourceUnavailableError(exc)
            else:
                err_count = 0

    def iter_docs(self, endpoint, collection=None):
        """
        Iterates over all documents of a given endpoint and collection.

        ``endpoint`` must be a valid endpoint at
        http://manager.scielo.org/api/v1/

        ``collection`` is a string of a valid name_slug. A complete
        list os collections is available at
        http://manager.scielo.org/api/v1/collections/

        Note that you need a valid API KEY in order to query the
        Manager API. Read more at: http://ref.scielo.org/ddkpmx
        """
        offset = 0
        limit = ITEMS_PER_REQUEST

        qry_params = {'offset': offset, 'limit': limit}
        if collection:
            qry_params.update({'collection': collection})

        while True:
            doc = self.fetch_data(endpoint, **qry_params)

            for obj in doc['objects']:
                # we are interested only in non-trashed items.
                if obj.get('is_trashed'):
                    continue

                yield obj

            if not doc['meta']['next']:
                raise StopIteration()
            else:
                offset += ITEMS_PER_REQUEST

    def get_all_journals(self, *collections):
        """
        Get all journals from the given collections

        ``collections`` is an arbitrary number of string values
        of valid name_slug attributes. A complete list os collections is
        available at http://manager.scielo.org/api/v1/collections/
        """
        journals = [self.iter_docs('journals', c) for c in collections]
        return itertools.chain(*journals)

    def get_all_collections(self):
        """
        Get all collections available at SciELO Manager.
        """
        return self.iter_docs('collections')
