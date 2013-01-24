# coding:utf8
from urlparse import urlparse

from django.conf import settings
import pymongo


MONGO_URI = getattr(settings, 'MONGO_URI',
    'mongodb://localhost:27017/journalmanager')


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
    exposed_api_methods = ['find', 'find_one']

    def __init__(self, doc, mongoconn_lib=MongoConnector, **kwargs):
        self._doc = doc

        # introspect the ``self._doc`` class to discover the collection name
        if 'mongo_collection' not in kwargs:
            kwargs['mongo_collection'] = self._doc._collection_name_

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
            setattr(cls, '_objects', self._mongomanager(cls,
                mongo_collection=self.collection, indexes=self.indexes))

        return cls._objects


class Document(object):

    def __init__(self, **kwargs):
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
        return Article(**cls.objects.find_one({'id': article_id}))


class Journal(Document):
    objects = ManagerFactory(collection='journals', indexes=['issue_ref'])

    def list_issues(self):
        """
        Iterates on all issues of the journal
        """

        for issue in self.issues:
            yield Issue(**issue['data'])


class Issue(Document):
    objects = ManagerFactory(collection='journals', indexes=['issues.id'])

    @classmethod
    def get_issue(cls, journal_id, issue_id):
        """
        Return a specific issue from a specific journal
        """

        return Issue(**cls.objects.find_one({'id': journal_id,
                                            'issues.id': issue_id},
                                            {'issues.data': 1})['data'])

    def list_articles(self):
        """
        Return a list of articles
        """

        for section in self.sections:
            for article_id in section['articles']:
                yield Article.get_article(article_id)

    def list_sections_articles(self, language):
        """
        Return a dictionary containing the sections and their corresponding
        articles
        Example:
            {'WHO Publications': [article_object]}
        """
        import collections

        sec_art = collections.OrderedDict()
        lst_art = list()

        for section in self.sections:
            journal_section = Section.get_section(self.id, section['id'])
            for article_id in section['articles']:
                lst_art.append(Article.get_article(article_id))
                sec_art[journal_section.get_section_title(language)] = lst_art
                yield sec_art


class Section(Document):
    objects = ManagerFactory(collection='journals', indexes=['sections.id'])

    @classmethod
    def get_section(cls, journal_id, section_id):
        """
        Return a specific section from a specific journal
        """

        return Section(**cls.objects.find_one({'id': journal_id,
                        'sections.id': section_id}))

    def get_section_title(self, language):
        """
        Return the title of a specific section
        """
        for title in self.titles:
            if language in title:
                return title[language]
