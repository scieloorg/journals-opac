# encoding: utf-8
import unittest

from django.test import TestCase
import pymongo

from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)

from catalog.mongomodels import Journal


class MongoManagerTest(MockerTestCase, TestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import MongoManager
        return MongoManager(*args, **kwargs)

    def test_make_db_available_on_instantiation(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles')

        self.assertIsInstance(mm._mongoconn.db, pymongo.database.Database)

    def test_instrospect_object_for_mongo_collection_discovery(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongo_collection='articles',
                           mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri)

        self.assertTrue(mm._mongoconn.col)

    def test_expose_pymongo_find_method(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_cursor = self.mocker.mock(pymongo.cursor.Cursor)

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        mongo_col.find()
        self.mocker.result(mongo_cursor)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles')

        self.assertIsInstance(mm.find(), pymongo.cursor.Cursor)

    def test_raw_access_to_pymongo_api(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        mongo_col.find()
        self.mocker.result([{'title': 'Some title'}])

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles')

        resultset = mm.find()
        for r in resultset:
            self.assertEqual(r, {'title': 'Some title'})

    def test_indexes_are_created(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index('issues_ref')
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles',
                           indexes=['issues_ref'])

        # the main idea is to assert that pymongo's
        # ensure_index() method is called, and mocker
        # asserts this to us. The assertion below is
        # just a placebo.
        self.assertTrue(True)

    def test_indexes_with_optional_params(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        mongo_db['articles']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index('acronym', unique=True)
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles',
                           indexes=[{'attr': 'acronym', 'unique': True}])

        # the main idea is to assert that pymongo's
        # ensure_index() method is called, and mocker
        # asserts this to us. The assertion below is
        # just a placebo.
        self.assertTrue(True)


class ManagersAutoDiscoveryTest(MockerTestCase, TestCase):

    def _makeCase1(self):
        import new
        from catalog.mongomodels import Document, MongoManager

        mocker_mongoconn = self.mocker.mock()
        mocker_mongoconn(KWARGS)
        self.mocker.result(mocker_mongoconn)
        self.mocker.replay()

        new_module = new.module('fake_module')

        class Foo(Document):
            objects = MongoManager(mongoconn_lib=mocker_mongoconn,
                mongo_collection='test')

        new_module.Foo = Foo

        return new_module

    def _makeCase2(self):
        import new
        from catalog.mongomodels import Document

        new_module = new.module('fake_module')

        class Foo(Document):
            objects = 'bla'

        new_module.Foo = Foo

        return new_module

    def _makeCase3(self):
        import new
        from catalog.mongomodels import MongoManager

        mocker_mongoconn = self.mocker.mock()
        mocker_mongoconn(KWARGS)
        self.mocker.result(mocker_mongoconn)
        self.mocker.replay()

        new_module = new.module('fake_module')

        class Foo(object):
            objects = MongoManager(mongoconn_lib=mocker_mongoconn,
                mongo_collection='test')

        new_module.Foo = Foo

        return new_module

    def test_mongomanager_instances_on_document_subclasses_are_identified(self):
        from catalog.mongomodels import _managers_autodiscover
        mod = self._makeCase1()

        self.assertEqual(_managers_autodiscover(base=mod), [mod.Foo.objects])

    def test_instances_different_than_mongomanager_are_ignored(self):
        from catalog.mongomodels import _managers_autodiscover
        mod = self._makeCase2()

        self.assertEqual(_managers_autodiscover(base=mod), [])

    def test_mongomanager_instances_on_not_document_subclasses_are_ignored(self):
        from catalog.mongomodels import _managers_autodiscover
        mod = self._makeCase3()

        self.assertEqual(_managers_autodiscover(base=mod), [])


class ArticleModelTest(MockerTestCase, TestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Article

        monkey_patches = kwargs.pop('monkeypatch', {})
        for attr, patch in monkey_patches.items():
            setattr(Article, attr, patch)

        return Article(*args, **kwargs)

    def test_simple_attr_access(self):
        article_microdata = {
            'title': 'Micronucleated lymphocytes in parents of lalala children'
        }

        a = self._makeOne(**article_microdata)

        self.assertEqual(a.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_simple_late_defined_attr(self):
        a = self._makeOne()

        a.title = 'Micronucleated lymphocytes in parents of lalala children'
        self.assertEqual(a.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_list_authors_must_return_a_lazy_object(self):
        from catalog.mongomodels import Article
        article_mock_objects = self.mocker.mock()

        article_authors_microdata = {
            "id": "AISS-JHjashA",
            "journal_id": "aiss",
            "contrib_group": {
                "author": [
                  {
                    "role": "ND",
                    "given_names": "Ahmet",
                    "surname": "Soysal",
                    "affiliations": [
                      "A01"
                    ]
                  },
                  {
                    "role": "ND",
                    "given_names": "Hatice",
                    "surname": "Simsek",
                    "affiliations": [
                      "A01"
                    ]
                  },
                  {
                    "role": "ND",
                    "given_names": "Dilek",
                    "surname": "Soysal",
                    "affiliations": [
                      "A02"
                    ]
                  },
                  {
                    "role": "ND",
                    "given_names": "Funda",
                    "surname": "Alyu",
                    "affiliations": [
                      "A03"
                    ]
                  }
                ]
            },
        }

        article_mock_objects.find_one({'id': 'AISS-JHjashA'})
        self.mocker.result(article_authors_microdata)

        self.mocker.replay()

        Article.objects = article_mock_objects

        article = Article.get_article('AISS-JHjashA')

        list_authors = article.list_authors()

        self.assertTrue(hasattr(list_authors, 'next'))
        author_1 = list_authors.next()
        self.assertEqual(author_1['given_names'], "Ahmet")
        author_2 = list_authors.next()
        self.assertEqual(author_2['surname'], "Simsek")

    @unittest.expectedFailure
    def test_needed_indexes_are_created(self):
        self.assertTrue(False)


class JournalModelTest(MockerTestCase, TestCase):

    def setUp(self):
        """
        Backup the original ``objects`` object ref.
        """
        self._original_objects = Journal.objects

    def tearDown(self):
        """
        Restore to the original ``objects`` object ref.
        """
        Journal.objects = self._original_objects

    def _makeOne(self, *args, **kwargs):

        return Journal(*args, **kwargs)

    def test_simple_attr_access(self):
        journal_microdata = {
            'title': 'Micronucleated lymphocytes in parents of lalala children'
        }

        j = self._makeOne(**journal_microdata)

        self.assertEqual(j.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_simple_late_defined_attr(self):
        j = self._makeOne()

        j.title = 'Micronucleated lymphocytes in parents of lalala children'
        self.assertEqual(j.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_list_issues_must_return_a_lazy_object(self):
        issues_data = {
            "id": 1,
            "issues": [
                {
                'id': 1,
                'data': {
                    "cover": None,
                    "created": "2010-04-01T01:01:01",
                    "ctrl_vocabulary": "nd",
                    "editorial_standard": "vancouv",
                    "id": 1,
                    "is_marked_up": False,
                    "is_press_release": False,
                    "is_trashed": False,
                    "label": "45 (4)",
                    "number": "4",
                    "order": 4,
                    "publication_end_month": 12,
                    "publication_start_month": 10,
                    "publication_year": 2009,
                    "resource_uri": "/api/v1/issues/1/",
                    "sections": [
                    {
                      "id": 514,
                      "articles": [
                        "AISS-JHjashA",
                      ]
                    }
                    ],
                    "suppl_number": None,
                    "suppl_volume": None,
                    "total_documents": 17,
                    "updated": "2012-11-08T10:35:37.193612",
                    "volume": "45"
                    }
                }
            ],
        }

        j = self._makeOne(**issues_data)

        issues = j.list_issues()
        self.assertTrue(hasattr(issues, 'next'))
        issue = issues.next()
        self.assertEqual(issue.editorial_standard, 'vancouv')

    def test_list_issues_must_return_a_reverse_list_order_by_year(self):
        from modelfactories import JournalFactory

        journal_microdata = [
                    {
                        "id": 1,
                        "data": {
                            "id": 1,
                            "label": "45 (4)",
                            "number": "4",
                            "publication_year": 2009,
                            "volume": "45",
                            "order": 1
                        }
                    },
                    {
                        "id": 2,
                        "data": {
                            "id": 2,
                            "label": "45 (5)",
                            "number": "5",
                            "publication_year": 2009,
                            "volume": "45",
                            "order": 2
                        }
                    },
                    {
                        "id": 4,
                        "data": {
                            "id": 4,
                            "label": "47 (1)",
                            "number": "1",
                            "publication_year": 2009,
                            "volume": "47",
                            "order": 3
                        }
                    },
                    {
                        "id": 3,
                        "data": {
                            "id": 3,
                            "label": "46 (1)",
                            "number": "1",
                            "publication_year": 2010,
                            "volume": "46",
                            "order": 4
                        }
                    },
                    {
                        "id": 5,
                        "data": {
                            "id": 5,
                            "label": "45 (10)",
                            "number": "10",
                            "publication_year": 2009,
                            "volume": "45",
                            "order": 5
                        }
                    },
                    {
                        "id": 6,
                        "data": {
                            "id": 6,
                            "label": "45 (3)",
                            "number": "3",
                            "publication_year": 2010,
                            "volume": "45",
                            "order": 6
                        }
                    },
                ]

        journal = JournalFactory.build(issues=journal_microdata)

        previous_year = 9999
        for issue in journal.list_issues():
            self.assertLessEqual(issue.publication_year, previous_year)
            previous_year = issue.publication_year

    @unittest.expectedFailure
    def test_needed_indexes_are_created(self):
        self.assertTrue(False)

    def test_get_journal_passing_journal_id(self):
        mock_objects = self.mocker.mock()

        journal_microdata = {
                  "contact": None,
                  "copyrighter": "Istituto Superiore di Sanità",
                  "cover": None,
                  "current_ahead_documents": 0,
                  "editor_address": "Viale Regina Elena 299",
                  "editor_address_city": "Rome",
                  "editor_address_country": "Italy",
                  "editor_address_state": None,
                  "editor_address_zip": "00161",
                  "editor_email": "annali@iss.it",
                  "editor_name": None,
                  "editor_phone1": "0039 06 4990 2945",
                  "editor_phone2": "0039 06 4990 2253",
                  "eletronic_issn": None,
                  "frequency": "Q",
                  "id": 1,
                  "languages": [
                    "en",
                    "it"
                  ],
                  "logo": None,
                  "missions": {
                    "en": "To disseminate information on researches in public health"
                  },
                  "other_previous_title": None,
                  "previous_ahead_documents": 0,
                  "print_issn": "0021-2571",
                  "pub_status": "current",
                  "pub_status_history": [
                    {
                      "date": "2010-04-01T00:00:00",
                      "status": "current"
                    }
                  ],
                  "publication_city": "Roma",
                  "publisher_country": "IT",
                  "publisher_name": "Istituto Superiore di Sanità",
                  "publisher_state": None,
                  "resource_uri": "/api/v1/journals/1/",
                  "scielo_issn": "print",
                  "short_title": "Ann. Ist. Super. Sanità",
                  "title": "Annali dell'Istituto Superiore di Sanità",
                  "title_iso": "Ann. Ist. Super. Sanità",
                  "url_journal": None,
                  "url_online_submission": None,
                  "use_license": {
                    "disclaimer": None,
                    "id": 1,
                    "license_code": None,
                    "reference_url": None,
                    "resource_uri": "/api/v1/uselicenses/1/"
                  },
                }

        mock_objects.find_one({'acronym': 'foo'})
        self.mocker.result(journal_microdata)

        self.mocker.replay()

        Journal.objects = mock_objects

        journal = Journal.get_journal(journal_id='foo')

        self.assertIsInstance(journal, Journal)
        self.assertEqual(journal.id, 1)

    def test_list_issue_by_year_must_return_a_lazy_object(self):
        from modelfactories import JournalFactory

        journal_microdata = [
                    {
                        "id": 1,
                        "data": {
                            "id": 1,
                            "label": "45 (4)",
                            "number": "4",
                            "publication_year": 2009,
                            "volume": "45",
                            "order": 1
                        }
                    },
                    {
                        "id": 2,
                        "data": {
                            "id": 2,
                            "label": "45 (5)",
                            "number": "5",
                            "publication_year": 2009,
                            "volume": "45",
                            "order": 2
                        }
                    },
                    {
                        "id": 4,
                        "data": {
                            "id": 4,
                            "label": "47 (1)",
                            "number": "1",
                            "publication_year": 2009,
                            "volume": "47",
                            "order": 3
                        }
                    },
                    {
                        "id": 3,
                        "data": {
                            "id": 3,
                            "label": "46 (1)",
                            "number": "1",
                            "publication_year": 2010,
                            "volume": "46",
                            "order": 4
                        }
                    },
                    {
                        "id": 5,
                        "data": {
                            "id": 5,
                            "label": "45 (10)",
                            "number": "10",
                            "publication_year": 2009,
                            "volume": "45",
                            "order": 5
                        }
                    },
                    {
                        "id": 6,
                        "data": {
                            "id": 6,
                            "label": "45 (3)",
                            "number": "3",
                            "publication_year": 2010,
                            "volume": "45",
                            "order": 6
                        }
                    },
                ]

        journal = JournalFactory.build(issues=journal_microdata)

        issues = journal.list_issues_as_grid()

        self.assertIn(2010, issues)
        self.assertTrue(len(issues) == 2)

    def test_address(self):
        from .modelfactories import JournalFactory

        journal = JournalFactory.build()
        address = journal.address

        self.assertEqual(address, "Viale Regina Elena 299, Rome, Rome, Italy")

    def test_address_with_missing_data(self):
        from .modelfactories import JournalFactory

        address_data = {
            "editor_address": "",
            "editor_address_city": None,
            "editor_address_country": "",
            "editor_address_state": "",
            }

        journal = JournalFactory.build(**address_data)
        address = journal.address

        self.assertEqual(address, None)

    def test_phones_with_many_entries(self):
        from .modelfactories import JournalFactory

        phone_data = {
            "editor_phone1": "0039 06 4990 2945",
            "editor_phone2": "0039 06 4990 2253",
            }

        journal = JournalFactory.build(**phone_data)
        phones = journal.phones

        self.assertEqual(phones, ['0039 06 4990 2945', '0039 06 4990 2253'])

    def test_phones_with_one_entry(self):
        from .modelfactories import JournalFactory

        phone_data = {
            "editor_phone1": "",
            "editor_phone2": "0039 06 4990 2253",
            }

        journal = JournalFactory.build(**phone_data)
        phones = journal.phones

        self.assertEqual(phones, ['0039 06 4990 2253'])

    def test_phones_with_zero_entries(self):
        from .modelfactories import JournalFactory

        phone_data = {
            "title": "AAA",
            "editor_phone1": "",
            "editor_phone2": "",
        }

        journal = JournalFactory.build(**phone_data)
        phones = journal.phones

        self.assertEqual(phones, [])

    def test_phones_with_missing_data(self):
        from .modelfactories import JournalFactory

        phone_data = {
            "editor_phone1": "",
            "editor_phone2": "",
            }

        journal = JournalFactory.build(**phone_data)
        phones = journal.phones

        self.assertEqual(phones, [])

    def test_phones_with_none_value(self):
        from .modelfactories import JournalFactory

        phone_data = {
            "editor_phone1": None,
            "editor_phone2": "",
            }

        journal = JournalFactory.build(**phone_data)
        phones = journal.phones

        self.assertEqual(phones, [])

    def test_scielo_issn_print_version(self):
        from .modelfactories import JournalFactory

        print_issn = {
            "scielo_issn": "print",
            "print_issn": "AAAA-AAAA",
            "eletronic_issn": "XXXX-XXXX"
            }

        journal = JournalFactory.build(**print_issn)
        issn = journal.issn

        self.assertEqual(issn, 'AAAA-AAAA')

    def test_scielo_issn_electronic_version(self):
        from .modelfactories import JournalFactory

        electronic_issn = {
            "scielo_issn": "electronic",
            "print_issn": "AAAA-AAAA",
            "eletronic_issn": "XXXX-XXXX"
            }

        journal = JournalFactory.build(**electronic_issn)
        issn = journal.issn

        self.assertEqual(issn, 'XXXX-XXXX')

    def test_list_journals(self):
        from catalog.mongomodels import list_journals, Journal

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.find({})
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.sort('_normalized_title', direction=pymongo.ASCENDING)
        self.mocker.result([{'title': 'Micronucleated lymphocytes in parents of lalala children'}])

        self.mocker.replay()

        journals = list_journals(mongomanager_lib=mock_mongomanager)
        for j in journals:
            self.assertTrue(isinstance(j, Journal))

    def test_list_journals_by_study_areas_returns_the_right_areas(self):
        from catalog.mongomodels import list_journals_by_study_areas

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.distinct('study_areas')
        self.mocker.result(['Zap', 'Zaz', 'Spam'])

        self.mocker.replay()

        journals = list_journals_by_study_areas(mongomanager_lib=mock_mongomanager)
        self.assertEqual([j['area'] for j in journals], ['Zap', 'Zaz', 'Spam'])

    def test_list_journals_by_study_areas_returns_valid_journals(self):
        from catalog.mongomodels import list_journals_by_study_areas, Journal

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)
        self.mocker.count(4)

        mock_mongomanager.distinct('study_areas')
        self.mocker.result(['Zap', 'Zaz', 'Spam'])

        mock_mongomanager.find({'study_areas': 'Zap'})
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.find({'study_areas': 'Zaz'})
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.find({'study_areas': 'Spam'})
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.sort('_normalized_title', direction=pymongo.ASCENDING)
        self.mocker.result([{'title': 'Micronucleated lymphocytes in parents of lalala children'}])
        self.mocker.count(3)

        self.mocker.replay()

        areas = list_journals_by_study_areas(mongomanager_lib=mock_mongomanager)
        for area in areas:
            for j in area['journals']:
                self.assertTrue(isinstance(j, Journal))

    def test_non_string_study_areas_are_ignored_on_list_journals_by_study_areas(self):
        from catalog.mongomodels import list_journals_by_study_areas

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)
        self.mocker.count(1)

        mock_mongomanager.distinct('study_areas')
        self.mocker.result([None, 'Zaz', 'Spam'])

        self.mocker.replay()

        areas = list_journals_by_study_areas(mongomanager_lib=mock_mongomanager)

        for area in areas:
            self.assertIn(area['area'], ['Zaz', 'Spam'])

    def test_issues_count_when_all_needed_data_exists(self):
        issues_data = {"issues": [{'id': 1}]}

        j = self._makeOne(**issues_data)
        self.assertEqual(j.issues_count, 1)

    def test_issues_count_when_issues_are_empty(self):
        issues_data = {'issues': []}

        j = self._makeOne(**issues_data)
        self.assertEqual(j.issues_count, 0)

    def test_issues_count_when_issues_are_missing(self):
        issues_data = {}

        j = self._makeOne(**issues_data)
        self.assertEqual(j.issues_count, 0)

    def test_journal_twitter_api_class_atribute(self):
        from catalog.mongomodels import Journal

        self.assertEqual(
            hasattr(Journal, '_twitter_api'),
            True)

    def test_tweets_valid_user(self):
        from .modelfactories import JournalFactory
        from catalog import mongomodels

        mock_twitter = self.mocker.mock()
        mock_tweet = self.mocker.mock()

        twitter_user = {
            "twitter_user": "redescielo"
            }

        mock_twitter.GetUserTimeline(ANY, page=0, count=3)
        self.mocker.result([mock_tweet])

        mock_tweet.text
        self.mocker.result(u'Novo peri\xf3dico na Cole\xe7\xe3o SciELO Brasil!')

        mock_tweet.created_at
        self.mocker.result(u'Mon Feb 04 13:41:19 +0000 2013')

        self.mocker.replay()

        # Testing valid twitter user
        journal = JournalFactory.build(**twitter_user)

        # monkeypatch a class attribute
        mongomodels.Journal._twitter_api = mock_twitter

        tweets = journal.tweets

        self.assertEqual(tweets[0]['text'],
                        u'Novo peri\xf3dico na Cole\xe7\xe3o SciELO Brasil!')
        self.assertEqual(tweets[0]['created_at'],
                        u'Mon Feb 04 13:41:19 +0000 2013')

    def test_tweets_invalid_user(self):
        from .modelfactories import JournalFactory
        from catalog import mongomodels
        from twitter import TwitterError

        mock_twitter = self.mocker.mock()

        twitter_user = {
            "twitter_user": "invalid_user"
            }

        mock_twitter.GetUserTimeline(ANY, page=0, count=3)
        self.mocker.throw(TwitterError)

        self.mocker.replay()

        # Testing valid twitter user
        journal = JournalFactory.build(**twitter_user)

        # monkeypatch a class attribute
        mongomodels.Journal._twitter_api = mock_twitter

        # Testing invalid twitter user
        tweets = journal.tweets

        self.assertEqual(tweets, [])


class IssueModelTest(MockerTestCase, TestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Issue
        return Issue(*args, **kwargs)

    def test_simple_attr_access(self):
        issue_microdata = {
            'title': 'foo bar'
        }

        i = self._makeOne(**issue_microdata)

        self.assertEqual(i.title,
            'foo bar')

    def test_simple_late_defined_attr(self):
        i = self._makeOne()

        i.title = 'fooisis barisis'
        self.assertEqual(i.title,
            'fooisis barisis')

    @unittest.expectedFailure
    def test_needed_indexes_are_created(self):
        self.assertTrue(False)

    def test_get_issue_passing_journal_id_and_issue_id(self):
        from catalog.mongomodels import Issue
        mock_objects = self.mocker.mock()

        issue_microdata = {
            "issues": [
                {
                    "id": 1,
                    "data": {
                        "cover": None,
                        "created": "2010-04-01T01:01:01",
                        "ctrl_vocabulary": "nd",
                        "editorial_standard": "vancouv",
                        "id": 1,
                        "is_marked_up": False,
                        "is_press_release": False,
                        "is_trashed": False,
                        "label": "45 (4)",
                        "number": "4",
                        "order": 4,
                        "publication_end_month": 12,
                        "publication_start_month": 10,
                        "publication_year": 2009,
                        "resource_uri": "/api/v1/issues/1/",
                        "sections": [
                        {
                          "id": 514,
                          "articles": [
                            "AISS-JHjashA",
                          ]
                        }
                        ],
                        "suppl_number": None,
                        "suppl_volume": None,
                        "total_documents": 17,
                        "updated": "2012-11-08T10:35:37.193612",
                        "volume": "45"
                    }
                }
            ]
        }

        mock_objects.find_one({'acronym': 'foo'}, {'issues': {'$elemMatch': {'id': 1}}})
        self.mocker.result(issue_microdata)

        self.mocker.replay()

        Issue.objects = mock_objects

        issue = Issue.get_issue(journal_id='foo', issue_id=1)

        self.assertIsInstance(issue, Issue)
        self.assertEqual(issue.total_documents, 17)
        self.assertEqual(issue.id, 1)

    def test_list_sections_from_issue_must_return_a_lazy_object(self):
        from catalog.mongomodels import Issue
        from catalog.mongomodels import Section
        from catalog.mongomodels import Article

        issue_mock_objects = self.mocker.mock()
        section_mock_objects = self.mocker.mock()
        article_mock_objects = self.mocker.mock()

        issue_section_microdata = {
            "acronym": "foo",
            "issues": [
                {
                    "id": 1,
                    "data": {
                        "cover": None,
                        "created": "2010-04-01T01:01:01",
                        "ctrl_vocabulary": "nd",
                        "editorial_standard": "vancouv",
                        "id": 1,
                        "is_marked_up": False,
                        "is_press_release": False,
                        "is_trashed": False,
                        "label": "45 (4)",
                        "number": "4",
                        "order": 4,
                        "publication_end_month": 12,
                        "publication_start_month": 10,
                        "publication_year": 2009,
                        "resource_uri": "/api/v1/issues/1/",
                        "sections": [
                        {
                          "id": 514,
                          "articles": [
                            "AISS-JHjashA",
                          ]
                        }
                        ],
                        "suppl_number": None,
                        "suppl_volume": None,
                        "total_documents": 17,
                        "updated": "2012-11-08T10:35:37.193612",
                        "volume": "45"
                    }
                }
            ],
            "sections": [
              {
                "id": 514,
                "data": {
                    "id": 514,
                    "resource_uri": "/api/v1/sections/514/",
                    "titles": [
                      {"en": "WHO Publications"}
                    ]
                }
              }
            ]
        }

        section_microdata = {
            "sections": [
                {
                  "id": 514,
                  "data": {
                      "id": 514,
                      "resource_uri": "/api/v1/sections/514/",
                      "titles": {
                        "en": "WHO Publications"
                      }
                  }
                }
            ]
        }

        article_microdata = {
            'id': 'AISS-JHjashA',
            'title': 'Micronucleated lymphocytes in parents of lalala children'
        }

        issue_mock_objects.find_one({'acronym': 'foo'}, {'issues': {'$elemMatch': {'id': 1}}})
        self.mocker.result(issue_section_microdata)

        section_mock_objects.find_one({'id': 1}, {'sections': {'$elemMatch': {'id': 514}}})
        self.mocker.result(section_microdata)

        article_mock_objects.find_one({'id': 'AISS-JHjashA'})
        self.mocker.result(article_microdata)

        self.mocker.replay()

        Issue.objects = issue_mock_objects
        Section.objects = section_mock_objects
        Article.objects = article_mock_objects

        issue = Issue.get_issue(journal_id='foo', issue_id=1)

        sections = issue.list_sections()

        self.assertTrue(hasattr(sections, 'next'))
        section = sections.next()
        self.assertEqual(section.id, 514)
        self.assertIsInstance(section.articles, list)
        self.assertIsInstance(section.articles[0], Article)


class SectionModelTest(MockerTestCase, TestCase):
    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Section
        return Section(*args, **kwargs)

    def test_get_section_passing_journal_id_and_section_id(self):
        from catalog.mongomodels import Section
        mock_objects = self.mocker.mock()

        section_microdata = {
            "sections": [
                {
                  "id": 514,
                  "data": {
                      "id": 514,
                      "resource_uri": "/api/v1/sections/514/",
                      "titles": {
                        "en": "WHO Publications"
                      }
                  }
                }
            ]
          }

        mock_objects.find_one({'id': 1}, {'sections': {'$elemMatch': {'id': 514}}})
        self.mocker.result(section_microdata)

        self.mocker.replay()

        Section.objects = mock_objects

        section = Section.get_section(journal_id=1, section_id=514)
        self.assertIsInstance(section, Section)
        self.assertEqual(section.resource_uri, '/api/v1/sections/514/')

    def test_get_section_title_by_language(self):
        from catalog.mongomodels import Section
        mock_objects = self.mocker.mock()

        section_microdata = {
            "sections": [
                {
                  "id": 514,
                  "data": {
                      "id": 514,
                      "resource_uri": "/api/v1/sections/514/",
                      "titles": {
                        "en": "WHO Publications"
                      }
                  }
                }
            ]
          }

        mock_objects.find_one({'id': 1}, {'sections': {'$elemMatch': {'id': 514}}})
        self.mocker.result(section_microdata)

        self.mocker.replay()

        Section.objects = mock_objects

        section = Section.get_section(journal_id=1, section_id=514)

        section_title = section.titles['en']

        self.assertEqual(section_title, 'WHO Publications')
