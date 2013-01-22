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

    def test_get_issue_passing_journal_id_and_issue_id(self):
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

        journal_data = {
            "abstract_keyword_languages": None,
            "acronym": "AISS",
            "collections": "/api/v1/collections/1/",
            "contact": None,
            "copyrighter": "Istituto Superiore di Sanità",
            "cover": None,
            "created": "2010-04-09T00:00:00",
            "creator": "/api/v1/users/1/",
            "ctrl_vocabulary": "nd",
            "current_ahead_documents": 0,
            "editor_address": "Viale Regina Elena 299, 00161 Italy Rome, Tel.: 0039 06 4990 2945, Fax: 0039 06 4990 2253",
            "editor_address_city": "",
            "editor_address_country": "",
            "editor_address_state": "",
            "editor_address_zip": "",
            "editor_email": "annali@iss.it",
            "editor_name": "",
            "editor_phone1": "",
            "editor_phone2": None,
            "editorial_standard": "vancouv",
            "eletronic_issn": "",
            "final_num": "",
            "final_vol": "",
            "final_year": None,
            "frequency": "Q",
            "id": 1,
            "index_coverage": "chemabs\nembase\nmedline\npascal\nzoological records",
            "init_num": "1",
            "init_vol": "1",
            "init_year": "1965",
            "is_indexed_aehci": False,
            "is_indexed_scie": False,
            "is_indexed_ssci": False,
            "issues": [
              {"id": 1,
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
            "languages": [
              "en",
              "it"
            ],
            "logo": None,
            "medline_code": None,
            "medline_title": None,
            "missions": [
              {"en": "To disseminate information on researches in public health"}
            ],
            "national_code": None,
            "notes": "",
            "other_previous_title": "",
            "other_titles": [],
            "previous_ahead_documents": 0,
            "print_issn": "0021-2571",
            "pub_level": "CT",
            "pub_status": "current",
            "pub_status_history": [
              {
                "date": "2010-04-01T00:00:00",
                "status": "current"
              }
            ],
            "pub_status_reason": "",
            "publication_city": "Roma",
            "publisher_country": "IT",
            "publisher_name": "Istituto Superiore di Sanità",
            "publisher_state": "",
            "resource_uri": "/api/v1/journals/1/",
            "scielo_issn": "print",
            "secs_code": "",
            "short_title": "Ann. Ist. Super. Sanità",
            "sponsors": [
              1
            ],
            "study_areas": [
              "Agricultural Sciences"
            ],
            "subject_descriptors": "public health",
            "title": "Annali dell'Istituto Superiore di Sanità",
            "title_iso": "Ann. Ist. Super. Sanità",
            "updated": "2012-11-08T10:35:00.448421",
            "url_journal": None,
            "url_online_submission": None,
            "use_license": {
              "disclaimer": "",
              "id": 1,
              "license_code": "",
              "reference_url": None,
              "resource_uri": "/api/v1/uselicenses/1/"
            },
            "sections": [
              {
                "id": 514,
                "resource_uri": "/api/v1/sections/514/",
                "titles": [
                  {"en": "WHO Publications"}
                ]
              }
            ]
          }

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        embedded_issue = self._makeOne(mongodb_driver=mongo_driver,
                              mongo_uri=mongo_uri,
                              **journal_data)

        issue = embedded_issue.get_issue(journal_data['id'],
                                         journal_data['issues'][0]['id'])

        self.assertEqual(issue.total_documents, 17)

    def test_list_article_id_from_issue_must_return_a_lazy_object(self):
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

        journal_data = {
            "abstract_keyword_languages": None,
            "acronym": "AISS",
            "collections": "/api/v1/collections/1/",
            "contact": None,
            "copyrighter": "Istituto Superiore di Sanità",
            "cover": None,
            "created": "2010-04-09T00:00:00",
            "creator": "/api/v1/users/1/",
            "ctrl_vocabulary": "nd",
            "current_ahead_documents": 0,
            "editor_address": "Viale Regina Elena 299, 00161 Italy Rome, Tel.: 0039 06 4990 2945, Fax: 0039 06 4990 2253",
            "editor_address_city": "",
            "editor_address_country": "",
            "editor_address_state": "",
            "editor_address_zip": "",
            "editor_email": "annali@iss.it",
            "editor_name": "",
            "editor_phone1": "",
            "editor_phone2": None,
            "editorial_standard": "vancouv",
            "eletronic_issn": "",
            "final_num": "",
            "final_vol": "",
            "final_year": None,
            "frequency": "Q",
            "id": 1,
            "index_coverage": "chemabs\nembase\nmedline\npascal\nzoological records",
            "init_num": "1",
            "init_vol": "1",
            "init_year": "1965",
            "is_indexed_aehci": False,
            "is_indexed_scie": False,
            "is_indexed_ssci": False,
            "issues": [
              {"id": 1,
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
            "languages": [
              "en",
              "it"
            ],
            "logo": None,
            "medline_code": None,
            "medline_title": None,
            "missions": [
              {"en": "To disseminate information on researches in public health"}
            ],
            "national_code": None,
            "notes": "",
            "other_previous_title": "",
            "other_titles": [],
            "previous_ahead_documents": 0,
            "print_issn": "0021-2571",
            "pub_level": "CT",
            "pub_status": "current",
            "pub_status_history": [
              {
                "date": "2010-04-01T00:00:00",
                "status": "current"
              }
            ],
            "pub_status_reason": "",
            "publication_city": "Roma",
            "publisher_country": "IT",
            "publisher_name": "Istituto Superiore di Sanità",
            "publisher_state": "",
            "resource_uri": "/api/v1/journals/1/",
            "scielo_issn": "print",
            "secs_code": "",
            "short_title": "Ann. Ist. Super. Sanità",
            "sponsors": [
              1
            ],
            "study_areas": [
              "Agricultural Sciences"
            ],
            "subject_descriptors": "public health",
            "title": "Annali dell'Istituto Superiore di Sanità",
            "title_iso": "Ann. Ist. Super. Sanità",
            "updated": "2012-11-08T10:35:00.448421",
            "url_journal": None,
            "url_online_submission": None,
            "use_license": {
              "disclaimer": "",
              "id": 1,
              "license_code": "",
              "reference_url": None,
              "resource_uri": "/api/v1/uselicenses/1/"
            },
            "sections": [
              {
                "id": 514,
                "resource_uri": "/api/v1/sections/514/",
                "titles": [
                  {"en": "WHO Publications"}
                ]
              }
            ]
          }

        mongo_uri = r'mongodb://user:pass@localhost:27017/journalmanager'
        embedded_issue = self._makeOne(mongodb_driver=mongo_driver,
                              mongo_uri=mongo_uri,
                              **journal_data)

        articles_id = embedded_issue.list_article_id(journal_id=journal_data['id'],
                                issue_id=journal_data['issues'][0]['id'])

        self.assertTrue(hasattr(articles_id, 'next'))
        article_id = articles_id.next()
        self.assertRegexpMatches(article_id, 'AISS-*')

    def test_list_sections_name_must_return_a_lazy_object(self):

