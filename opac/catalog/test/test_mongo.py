# coding: utf8
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

        self.assertIsInstance(mm.db, pymongo.database.Database)

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

        self.assertTrue(mm.col)

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


class ArticleModelTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Article
        return Article(*args, **kwargs)

    def test_simple_attr_access(self):
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

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

        article_microdata = {
            'title': 'Micronucleated lymphocytes in parents of lalala children'
        }

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        a = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri,
                          **article_microdata)

        self.assertEqual(a.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_simple_late_defined_attr(self):
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

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        a = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri)

        a.title = 'Micronucleated lymphocytes in parents of lalala children'
        self.assertEqual(a.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_needed_indexes_are_created(self):
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

        mongo_col.ensure_index('issue_ref')
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        a = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri)

        self.assertTrue(True) # placebo


class JournalModelTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Journal
        return Journal(*args, **kwargs)

    def test_simple_attr_access(self):
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

        mongo_db['journals']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

        journal_microdata = {
            'title': 'Micronucleated lymphocytes in parents of lalala children'
        }

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        j = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri,
                          **journal_microdata)

        self.assertEqual(j.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_simple_late_defined_attr(self):
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

        mongo_db['journals']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        j = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri)

        j.title = 'Micronucleated lymphocytes in parents of lalala children'
        self.assertEqual(j.title,
            'Micronucleated lymphocytes in parents of lalala children')

    def test_list_issues_must_return_a_lazy_object(self):
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

        mongo_db['journals']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

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

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        j = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri,
                          **issues_data)

        issues = j.list_issues()
        self.assertTrue(hasattr(issues, 'next'))
        issue = issues.next()
        self.assertEqual(issue.editorial_standard, 'vancouv')


class IssueModelTest(TestCase, MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from catalog.mongomodels import Issue
        return Issue(*args, **kwargs)

    def test_simple_attr_access(self):
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

        mongo_db['journals']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

        issue_microdata = {
            'title': 'foo bar'
        }

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        i = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri,
                          **issue_microdata)

        self.assertEqual(i.title,
            'foo bar')

    def test_simple_late_defined_attr(self):
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

        mongo_db['journals']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index(ANY)
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        i = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri)

        i.title = 'fooisis barisis'
        self.assertEqual(i.title,
            'fooisis barisis')

    def test_needed_indexes_are_created(self):
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

        mongo_db['journals']
        self.mocker.result(mongo_col)

        mongo_col.ensure_index('issues.id')
        self.mocker.result(None)

        self.mocker.replay()

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        a = self._makeOne(mongodb_driver=mongo_driver,
                          mongo_uri=mongo_uri)

        self.assertTrue(True) # placebo
