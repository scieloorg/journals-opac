# coding:utf8
from urlparse import urlparse

from django.conf import settings
import pymongo

import twitter
from twitter import TwitterError


MONGO_URI = getattr(settings, 'MONGO_URI',
    'mongodb://localhost:27017/journalsopac')


class DbOperationsError(Exception):
    """Represents all possible exceptions while interacting with
    MongoDB.
    """


class MongoConnector(object):
    """
    Connects to MongoDB and makes self.db and self.col
    available to the instance.
    """

    def __init__(self, mongodb_driver=pymongo,
                       mongo_uri=MONGO_URI,
                       mongo_collection=None):
        db_url = urlparse(mongo_uri)
        self._conn = mongodb_driver.Connection(host=db_url.hostname,
                                               port=db_url.port)
        self.db = self._conn[db_url.path[1:]]
        if db_url.username and db_url.password:
            self.db.authenticate(db_url.username, db_url.password)

        self.col = self.db[mongo_collection] if mongo_collection else None

        #  ensure indexes if they exist
        if hasattr(self, '_ensure_indexes'):
            self._ensure_indexes()


class MongoManager(object):
    """
    Wraps a subset of pymongo.collection.Collection methods, in order
    to act as a manager for mongodb documents. The collection must be
    set, in instantiation, using the ``mongo_collection`` arg.

    The exposed methods must be in the ``exposed_api_methods`` list.

    See the pymongo docs for more information about using the exposed
    methods:
    http://api.mongodb.org/python/current/api/pymongo/collection.html
    """
    exposed_api_methods = ['find', 'find_one', 'distinct']

    def __init__(self, mongoconn_lib=MongoConnector, **kwargs):

        if 'mongo_collection' not in kwargs:
            raise ValueError('missing mongo_collection')

        indexes = kwargs.pop('indexes', [])

        self._mongoconn = mongoconn_lib(**kwargs)

        # ensure all needed mongodb indexes had been created
        if indexes:
            self._ensure_indexes(indexes)

    def __getattr__(self, name):

        if name in self.exposed_api_methods:
            if not self._mongoconn.col:
                raise ValueError(
                    'method %s needs a collection to be defined' % name)

            if hasattr(self._mongoconn.col, name):
                return getattr(self._mongoconn.col, name)
            else:
                raise AttributeError()
        else:
            raise AttributeError()

    def _ensure_indexes(self, indexes):
        for index in indexes:
            self._mongoconn.col.ensure_index(index)


class ManagerFactory(object):

    def __init__(self, collection,
                       indexes,
                       mongomanager_lib=MongoManager):
        self.collection = collection
        self.indexes = indexes
        self._mongomanager = mongomanager_lib

    def __get__(self, instance, cls):
        if not hasattr(cls, '_objects'):
            setattr(cls, '_objects', self._mongomanager(
                mongo_collection=self.collection, indexes=self.indexes))

        return cls._objects


class Document(object):

    def __init__(self, **kwargs):
        self._data = {}

        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __setattr__(self, name, value):
        _data = self.__dict__.setdefault('_data', {})
        _data[name] = value

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (self.__class__, name)
            )


class Article(Document):
    objects = ManagerFactory(collection='articles', indexes=['issue_ref'])

    @property
    def original_title(self):
        try:
            return self._data['title-group'][self._data['default-language']]
        except KeyError:
            return u''

    @classmethod
    def get_article(cls, article_id):
        """
        Return the article by id
        """
        return Article(**cls.objects.find_one({'id': article_id}))

    def list_authors(self):
        for author in self.contrib_group['author']:
            yield author


def list_journals(criteria=None, mongomanager_lib=MongoManager):
    """
    Lists all journals present in a collection

    ``criteria`` is a dict of query params, in the form::

        list_journals(criteria={'study_areas': 'Natural Sciences'})
    """
    mm = mongomanager_lib(mongo_collection='journals')

    criteria = {} if criteria is None else criteria

    if not isinstance(criteria, dict):
        raise ValueError('criteria must be dict')

    for result in mm.find(criteria).sort('_normalized_title',
        direction=pymongo.ASCENDING):
        yield Journal(**result)


def list_journals_by_study_areas(mongomanager_lib=MongoManager):
    """
    Lists all journals by study area, returning the following format::

        [{'area': 'Agricultural Sciences', 'journals': [<journal 1>]}]
    """
    mm = mongomanager_lib(mongo_collection='journals')

    areas = mm.distinct('study_areas')

    areas_list = []
    for area in areas:
        item = {
            'area': area,
            'journals': list_journals(criteria={'study_areas': area},
                                      mongomanager_lib=mongomanager_lib)
        }
        areas_list.append(item)

    return areas_list


def list_press_releases(journal_id, mongomanager_lib=MongoManager):
    """
    Lists the last 10 press releases from a specific journal
    """
    mm = mongomanager_lib(mongo_collection='journals')

    for issue in mm.find({'journal_id': journal_id,
        'issues.data.is_press_release': True},
        {'issues.data': 1})[0]['issues']:

        yield issue


class Journal(Document):
    objects = ManagerFactory(collection='journals',
        indexes=['issue_ref', 'title', 'study_areas', 'id'])

    _twitter_api = twitter.Api()

    @classmethod
    def get_journal(cls, journal_id):
        """
        Return a specific journal
        """

        journal = cls.objects.find_one({'id': int(journal_id)})

        if journal:
            return cls(**journal)

        raise ValueError('no journal found for id:'.format(journal_id))

    def list_issues(self):
        """
        Iterates on all issues of the journal
        """

        for issue in self.issues:
            yield Issue(**issue['data'])

    @property
    def issues_count(self):
        try:
            return len(self.issues)
        except AttributeError:
            return 0

    @property
    def address(self):
        """
        This method retrives a string with the editor address
        within the journal register.
        """

        address = []
        if 'editor_address' in self._data:
            if self._data['editor_address'] != None and self._data['editor_address'].strip():
                address.append(self._data['editor_address'])

        if 'editor_address_city' in self._data:
            if self._data['editor_address_city'] != None and self._data['editor_address_city'].strip():
                address.append(self._data['editor_address_city'])

        if 'editor_address_state' in self._data:
            if self._data['editor_address_state'] != None and self._data['editor_address_state'].strip():
                address.append(self._data['editor_address_state'])

        if 'editor_address_country' in self._data:
            if self._data['editor_address_country'] != None and self._data['editor_address_country'].strip():
                address.append(self._data['editor_address_country'])

        address_string = ', '.join(address)

        if address_string.strip():
            return address_string.strip()

    @property
    def tweets(self):
        """
        Retrieve a list of tweets from a specific users
        defined into the journal metadata.
        """

        tweets = []
        if self._data.get('twitter_user'):

            try:
                tws = self._twitter_api.GetUserTimeline(
                    self._data['twitter_user'], page=0, count=3)
            except TwitterError:
                return tweets

            for tw in tws:
                tweets.append({'text': tw.text,
                               'created_at': tw.created_at})

        return tweets

    @property
    def phones(self):
        """
        This method retrives a list of phone numbers
        within the journal register.
        """
        phones = []

        if 'editor_phone1' in self._data:
            if self._data['editor_phone1'] != None and len(self._data['editor_phone1'].strip()) > 0:
                phones.append(self._data['editor_phone1'])

        if 'editor_phone2' in self._data:
            if self._data['editor_phone2'] != None and len(self._data['editor_phone2'].strip()) > 0:
                phones.append(self._data['editor_phone2'])

        return phones

    @property
    def issn(self):
        """
        This method retrieves the issn number according with the
        value indicated into the field scielo_issn.
        """
        issn = None

        if self._data['scielo_issn'] == 'print':
            issn = self._data['print_issn']
        else:
            issn = self._data['eletronic_issn']

        return issn


class Issue(Document):
    objects = ManagerFactory(collection='journals', indexes=['issues.id'])

    @classmethod
    def get_issue(cls, journal_id, issue_id):
        """
        Return a specific issue from a specific journal
        """

        issue = cls.objects.find_one({'id': journal_id,
                                      'issues.id': issue_id},
                                      {'issues.data': 1})['data']
        if issue:
            return cls(**issue)

        raise ValueError('no issue found for id:'.format(journal_id))

    def list_sections(self):
        """
        Return a list of sections and their related articles
        """

        articles_list = []

        for issue_section in self.sections:
            journal_section = Section.get_section(self.id, issue_section['id'])

            for article_id in issue_section['articles']:
                articles_list.append(Article.get_article(article_id))

            journal_section.articles = articles_list
            yield journal_section


class Section(Document):
    objects = ManagerFactory(collection='journals', indexes=['sections.id'])

    @classmethod
    def get_section(cls, journal_id, section_id):
        """
        Return a specific section from a specific journal
        """
        return Section(**cls.objects.find_one({'id': journal_id,
                        'sections.id': section_id}, {'sections.data': 1})['data'])
