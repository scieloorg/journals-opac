# coding:utf8
from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.conf import settings
from collections import OrderedDict
import pymongo

import twitter
from twitter import TwitterError


MONGO_URI = getattr(settings, 'MONGO_URI',
    'mongodb://localhost:27017/journalsopac')


class DbOperationsError(Exception):
    """Represents all possible exceptions while interacting with
    MongoDB.
    """


class DocDoesNotExist(Exception):
    """
    Equivalent to Django's DoesNotExist. It is raised when operations
    that needs the objects to be saved are called on unsaved objects.
    """


def ensure_exists(method):
    """
    Decorator to be used on methods of Document subclasses, to sign
    that the method can only be called on saved documents.
    """
    def decorator(instance, *args, **kwargs):
        if not '_id' in instance._data:
            raise DocDoesNotExist('the document must be saved')

        return method(instance, *args, **kwargs)

    return decorator


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
            if isinstance(index, dict):
                attr = index.pop('attr')
                self._mongoconn.col.ensure_index(attr, **index)
                continue

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
        # try to avoid None values that may have scaped from previous
        # cleanups.
        if not isinstance(area, basestring):
            continue

        item = {
            'area': area,
            'journals': list_journals(criteria={'study_areas': area},
                                      mongomanager_lib=mongomanager_lib)
        }
        areas_list.append(item)

    return areas_list


class Journal(Document):
    objects = ManagerFactory(collection='journals', indexes=[
        'issue_ref', 'title', 'study_areas', 'id',
        {'attr': 'acronym', 'unique': True}
    ])

    _twitter_api = twitter.Api()

    @classmethod
    def get_journal(cls, journal_id):
        """
        Return a specific journal
        """

        journal = cls.objects.find_one({'acronym': journal_id})

        if not journal:
            raise ValueError('no journal found for id:'.format(journal_id))

        return cls(**journal)

    def list_issues(self):
        """
        Iterates on all issues of the journal order by publication_year
        """

        for issue in sorted(self.issues, key=lambda x: x['data']['publication_year'], reverse=True):
            yield Issue(**issue['data'])

    def list_issues_as_grid(self):
        """
        Return a list of issues group by year

        Example:
            issues = OrderedDict(
                '2009':  {'45': [issue_object, issue_object, issue_object, ]})
        """

        grid = OrderedDict()

        for issue in self.list_issues():
            year_node = grid.setdefault(issue.publication_year, {})
            volume_node = year_node.setdefault(issue.volume, [])
            volume_node.append(issue)

        for year, volume in grid.items():
            for vol, issues in volume.items():
                issues.sort(key=lambda x: x.order)

        return grid

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
        if self._data.get('editor_address'):
            address.append(self._data['editor_address'])

        if self._data.get('editor_address_city'):
            address.append(self._data['editor_address_city'])

        if self._data.get('editor_address_state'):
            address.append(self._data['editor_address_state'])

        if self._data.get('editor_address_country'):
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

        if self._data.get('editor_phone1'):
            phones.append(self._data['editor_phone1'])

        if self._data.get('editor_phone2'):
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

    @ensure_exists
    def get_absolute_url(self):
        return reverse('catalog.journal', kwargs={'journal_id': self.acronym})

    @property
    def current_issue(self):
        """
        This method retrives a link to the current issue from a
        given journal.
        """

        last = max(self.list_issues(), key=lambda x: x.order)

        return last.id


class Navigation(object):

    def __init__(self, journal):

        self._issues = dict((issue['data']['order'], issue['data']['id']) for issue in journal.issues)

    def next_issue(self, current_order):
        """
        This method retrieves the next issue id according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        for i in range(1, 100):
            match = current_order + i
            next = self._issues.get(match)
            if next:
                return next

        return None

    def previous_issue(self, current_order):
        """
        This method retrieves the previous issue id according to the
        order sequence. If there is a gap in the issues sequence,
        for legacy compliance, the script will attempt a 100 different
        order numbers before delivery "None".
        """
        for i in range(1, 100):
            match = current_order - i

            if match == 0:
                break

            previous = self._issues.get(match)
            if previous:
                return previous

        return None


class Issue(Document):
    objects = ManagerFactory(collection='journals', indexes=['issues.id'])

    @classmethod
    def get_issue(cls, journal_id, issue_id):
        """
        Return a specific issue from a specific journal
        """

        issue = cls.objects.find_one({'acronym': journal_id},
                                     {'issues': {'$elemMatch': {'id': int(issue_id)}}})['issues'][0]['data']

        if not issue:
            raise ValueError('no issue found for id:'.format(journal_id))

        issue['acronym'] = journal_id

        return cls(**issue)

    @property
    def journal(self):
        """
        This method retrieves the journal related to issue instance.
        """

        journal = Journal.get_journal(journal_id=self._data['acronym'])

        return journal

    @property
    def previous_issue(self):
        """
        This method retrives an id to the previous issue from a
        given journal.
        """
        journal = Journal.get_journal(journal_id=self._data['acronym'])

        nav = Navigation(journal)

        return nav.previous_issue(self._data['order'])

    @property
    def next_issue(self):
        """
        This method retrives an id to the previous issue from a
        given journal.
        """
        journal = Journal.get_journal(journal_id=self._data['acronym'])

        nav = Navigation(journal)

        return nav.next_issue(self._data['order'])

    def list_sections(self):
        """
        Return a list of sections and their related articles
        """

        for issue_section in self.sections:
            journal_section = Section.get_section(self.id, issue_section['id'])

            articles_list = []
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

        section = cls.objects.find_one({'id': journal_id},
                                       {'sections': {'$elemMatch': {'id': int(section_id)}}})['sections'][0]['data']

        if not section:
            raise ValueError('no section found for id:'.format(journal_id))

        return Section(**section)
