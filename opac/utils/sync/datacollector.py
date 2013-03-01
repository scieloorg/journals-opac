# coding: utf-8
import logging
import time
import itertools
import copy

from django.conf import settings
import slumber
import requests

from catalog import mongomodels


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

    def iter_docs(self, endpoint, collection=None, **kwargs):
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

        kwargs.update({'limit': limit})
        if collection:
            kwargs.update({'collection': collection})

        while True:
            kwargs.update({'offset': offset})
            doc = self.fetch_data(endpoint, **kwargs)

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

    def get_journals(self, *journals):
        """
        Get all the given journals

        ``journals`` is an arbitrary number of string values
        of resource_ids.
        """
        for j in journals:
            yield self.fetch_data('journals', resource_id=j)

    def get_all_collections(self):
        """
        Get all collections available at SciELO Manager.
        """
        return self.iter_docs('collections')

    def get_changes(self, since=0):
        return self.iter_docs('changes', since=since)

    def get_issues(self, *issues):
        """
        Get all the given issues

        ``issues`` is an arbitrary number of string values
        of resource_ids.
        """
        for i in issues:
            yield self.fetch_data('issues', resource_id=i)


def _list_issues_uri(journal_meta, journal_dep=mongomodels.Journal):
        # TODO: This instantiation logic must be at Journal.get_journal
        journal_data = journal_dep.objects.find_one({'id': journal_meta.resource_id})

        if not journal_data:
            raise ValueError('invalid id for Journals: %s' % journal_meta.resource_id)

        journal_doc = journal_dep(**journal_data)

        return (issue.resource_uri for issue in journal_doc.list_issues())


class ChangeListIterator(object):
    def __init__(self, data):
        self._data = sorted(copy.deepcopy(data), key=lambda x: x.seq)
        self._index = -1

    def __iter__(self):
        return self

    def next(self):
        self._index += 1
        try:
            return self._data[self._index]
        except IndexError:
            raise StopIteration()


class ChangesList(object):

    def __init__(self, data, list_issues_uri_dep=_list_issues_uri):
        self._changes = []

        for event in data:
            if isinstance(event, dict):
                self._changes.append(Change(**event))
            elif isinstance(event, Change):
                self._changes.append(event)
            else:
                raise TypeError()

        self.list_issues_uri = list_issues_uri_dep

    def filter(self, collections=None, journals=None):
        """
        Produces another ChangesList instance containing only
        Changes that match the expectations.
        """
        journals_list = []
        issues_list = []

        # list uris from all journals and its issues
        if journals:
            for j in journals:
                journals_list.append(j.resource_uri)
                issues_list.append(self.list_issues_uri(j))

        journals_uris = set(journals_list)
        issues_uris = set(itertools.chain(*issues_list))

        if collections:
            collections_uris = set(c.resource_uri for c in collections)
        else:
            collections_uris = []

        superset = set().union(journals_uris, issues_uris, collections_uris)

        changes = []
        for change in self:
            _collection_uri = change.collection_uri
            _object_uri = change.object_uri

            if _collection_uri in superset or _object_uri in superset:
                changes.append(change)

        return ChangesList(changes)

    def __iter__(self):
        return ChangeListIterator(self._changes)


class Change(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
