# coding: utf8
import unittest

from django.test import TestCase
import pymongo
from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)


class MongoManagerTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import MongoManager
        return MongoManager(*args, **kwargs)

    def test_make_db_available_on_instantiation(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()
        article = self.mocker.mock()

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
        mm = self._makeOne(article,
                           mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles')

        self.assertIsInstance(mm._mongoconn.db, pymongo.database.Database)

    def test_instrospect_object_for_mongo_collection_discovery(self):
        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()
        article = self.mocker.mock()

        mongo_driver.Connection(host=ANY, port=ANY)
        self.mocker.result(mongo_conn)

        mongo_conn[ANY]
        self.mocker.result(mongo_db)

        mongo_db.authenticate(ANY, ANY)
        self.mocker.result(None)

        article._collection_name_
        self.mocker.result('articles')

        mongo_db['articles']
        self.mocker.result(mongo_col)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        mm = self._makeOne(article,
                           mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri)

        self.assertTrue(mm._mongoconn.col)

    def test_expose_pymongo_find_method(self):
        from catalog.mongomodels import Article

        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()
        article = self.mocker.mock(Article)
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
        mm = self._makeOne(article,
                           mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles')

        self.assertIsInstance(mm.find(), pymongo.cursor.Cursor)

    def test_raw_access_to_pymongo_api(self):
        from catalog.mongomodels import Article

        mongo_driver = self.mocker.mock()
        mongo_conn = self.mocker.mock()
        mongo_db = self.mocker.mock(pymongo.database.Database)
        mongo_col = self.mocker.mock()
        article = self.mocker.mock(Article)

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
        mm = self._makeOne(article,
                           mongodb_driver=mongo_driver,
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
        article = self.mocker.mock()

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
        mm = self._makeOne(article,
                           mongodb_driver=mongo_driver,
                           mongo_uri=mongo_uri,
                           mongo_collection='articles',
                           indexes=['issues_ref'])

        # the main idea is to assert that pymongo's
        # ensure_index() method is called, and mocker
        # asserts this to us. The assertion below is
        # just a placebo.
        self.assertTrue(True)


class ArticleModelTest(TestCase, MockerTestCase):

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

    @unittest.expectedFailure
    def test_needed_indexes_are_created(self):
        self.assertTrue(False)


class JournalModelTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Journal
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

    @unittest.expectedFailure
    def test_needed_indexes_are_created(self):
        self.assertTrue(False)


class IssueModelTest(TestCase, MockerTestCase):

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

        mock_objects.find_one({'id': 1, 'issues.id': 1}, {'issues.data': 1})
        self.mocker.result(issue_microdata)

        self.mocker.replay()

        Issue.objects = mock_objects

        issue = Issue.get_issue(journal_id=1, issue_id=1)

        self.assertIsInstance(issue, Issue)
        self.assertEqual(issue.total_documents, 17)
        self.assertEqual(issue.id, 1)

    def test_list_sections_from_issue_must_return_a_lazy_object(self):
        from catalog.mongomodels import Issue
        from catalog.mongomodels import Section

        issue_mock_objects = self.mocker.mock()
        section_mock_objects = self.mocker.mock()

        issue_section_microdata = {
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
            },
            "sections": [
            {
              "id": 514,
              "resource_uri": "/api/v1/sections/514/",
              "titles": [
                {"en": "WHO Publications"}
              ]
            }
            ],
        }

        section_microdata = {
              "id": 514,
              "resource_uri": "/api/v1/sections/514/",
              "titles": [
                {"en": "WHO Publications"}
              ]
        }

        issue_mock_objects.find_one({'id': 1, 'issues.id': 1}, {'issues.data': 1})
        self.mocker.result(issue_section_microdata)

        section_mock_objects.find_one({'id': 1, 'sections.id': 514})
        self.mocker.result(section_microdata)

        self.mocker.replay()

        Issue.objects = issue_mock_objects
        Section.objects = section_mock_objects

        issue = Issue.get_issue(journal_id=1, issue_id=1)

        sections = issue.list_sections()

        self.assertTrue(hasattr(sections, 'next'))
        section = sections.next()
        self.assertEqual(section.id, 514)
        self.assertEqual(section.get_title('en'), 'WHO Publications')
        self.assertIsInstance(section.articles, list)
        self.assertTrue(section.articles[0], 'AISS-JHjashA')


class SectionModelTest(TestCase, MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Section
        return Section(*args, **kwargs)

    def test_get_section_passing_journal_id_and_section_id_and_language(self):
        from catalog.mongomodels import Section
        mock_objects = self.mocker.mock()

        section_microdata = {
              "id": 514,
              "resource_uri": "/api/v1/sections/514/",
              "titles": [
                {"en": "WHO Publications"}
              ]
        }

        mock_objects.find_one({'id': 1, 'sections.id': 514})
        self.mocker.result(section_microdata)

        self.mocker.replay()

        Section.objects = mock_objects

        section = Section.get_section(journal_id=1, section_id=514)
        self.assertIsInstance(section, Section)
        self.assertEqual(section.get_title('en'), 'WHO Publications')

    def test_get_section_title_by_language(self):
        from catalog.mongomodels import Section
        mock_objects = self.mocker.mock()

        section_microdata = {
              "id": 514,
              "resource_uri": "/api/v1/sections/514/",
              "titles": [
                {"en": "WHO Publications"}
              ]
        }

        mock_objects.find_one({'id': 1, 'sections.id': 514})
        self.mocker.result(section_microdata)

        self.mocker.replay()

        Section.objects = mock_objects

        section = Section.get_section(journal_id=1, section_id=514)

        section_title = section.get_title('en')

        self.assertEqual(section_title, 'WHO Publications')
