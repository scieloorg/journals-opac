# encoding: utf-8
from collections import OrderedDict
from django.test import TestCase

from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)


class NavigationTest(MockerTestCase):

    def test_instatiation_with_issue(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 1,
                    u'id': 4,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 3,
                    u'id': 6,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 5,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 2,
                    u'id': 5,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build()

        nav = Navigation(journal, issue=issue)
        self.assertEqual(nav._issue, issue)

    def test_instatiation_without_issue(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        mock_issue = self.mocker.mock()

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 1,
                    u'id': 4,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 3,
                    u'id': 6,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 5,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 2,
                    u'id': 5,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            }
        ]

        issue = IssueFactory.build()
        mock_issue.get_issue(ANY, ANY)
        self.mocker.result(issue)
        self.mocker.replay()

        journal = JournalFactory.build(issues=issues)

        nav = Navigation(journal, issue_lib=mock_issue)
        nav._load_issue()

        self.assertEqual(nav._issue, issue)

    def test_journal_with_ahead(self):
        from .modelfactories import JournalFactory
        from catalog.tools import Navigation

        journal_data = {
                            u'current_ahead_documents': 10,
                        }

        journal = JournalFactory.build(**journal_data)

        nav = Navigation(journal).ahead

        self.assertEqual(nav, '/ahead/AISS/')

    def test_journal_without_ahead(self):
        from .modelfactories import JournalFactory
        from catalog.tools import Navigation

        journal = JournalFactory.build()

        nav = Navigation(journal).ahead

        self.assertEqual(nav, None)

    def test_current_issue(self):
        from .modelfactories import JournalFactory
        from catalog.tools import Navigation

        issues = [
                {
                'id': 2,
                'data': {
                    "created": "2010-04-01T01:01:01",
                    "id": 2,
                    "label": "45 (5)",
                    "order": 5,
                    "total_documents": 3,
                    "updated": "2012-11-08T10:35:37.193612",
                    "publication_year": 2005,
                    "volume": '46'
                    }
                },
                {
                'id': 3,
                'data': {
                    "id": 3,
                    "label": "45 (6)",
                    "order": 6,
                    "total_documents": 3,
                    "updated": "2012-11-08T10:35:37.193612",
                    "publication_year": 2005,
                    "volume": '47'
                    }
                }
            ]

        journal = JournalFactory.build(issues=issues)

        nav = Navigation(journal).current_issue

        self.assertEqual(nav, '/issue/AISS/3/')

    def test_get_next_issue_id(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 1,
                            u'id': 4,
                            u'publication_year': 2005,
                            u'volume': '47'
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 1,
                    u'id': 4,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'order': 3,
                    u'id': 6,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).next_issue

        self.assertEqual(nav, '/issue/AISS/6/')

    def test_get_previous_issue_id(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 3,
                            u'id': 6,
                            u'publication_year': 2005,
                            u'volume': '47'
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 1,
                    u'id': 4,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'order': 3,
                    u'id': 6,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).previous_issue

        self.assertEqual(nav, '/issue/AISS/4/')

    def test_get_next_issue_from_current_must_return_none(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 3,
                            u'id': 5,
                            u'publication_year': 2005,
                            u'volume': '47'
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 1,
                    u'id': 4,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'order': 2,
                    u'id': 6,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 7,
                u'data':
                {
                    u'order': 3,
                    u'id': 5,
                    u'publication_year': 2005,
                    u'volume': '47'
                }
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).next_issue

        self.assertEqual(nav, None)

    def test_get_previous_from_first_issue_must_return_none(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 1,
                            u'id': 5,
                            u'publication_year': 2005,
                            u'volume': '47'
                        }

        issues = [
            {
                u'id': 3,
                u'data':
                {
                    u'order': 1,
                    u'id': 5,
                    u'publication_year': 2005,
                    u'volume': '47'
                }
            },
            {
                u'id': 4,
                u'data':
                {
                    u'order': 2,
                    u'id': 4,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'order': 3,
                    u'id': 6,
                    u'publication_year': 2005,
                    u'volume': '47'
                },
            },
            {
                u'id': 7,
                u'data':
                {
                    u'order': 4,
                    u'id': 7,
                    u'publication_year': 2005,
                    u'volume': '47'
                }
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).previous_issue

        self.assertEqual(nav, None)


class TryGetContentByLangTest(TestCase):

    def test_try_get_content_by_lang(self):
        from catalog.tools import try_get_content_by_lang

        test_micro_data = {
            "en": "Management of health-care waste in Izmir, Turkey",
            "it": "Gestione dei rifiuti sanitari in Izmir, Turchia"
        }

        content = try_get_content_by_lang(test_micro_data, 'en')

        self.assertEqual(content, 'Management of health-care waste in Izmir, Turkey')

    def test_try_get_content_by_lang_must_raise_error_when_param_not_dict(self):
        from catalog.tools import try_get_content_by_lang

        test_micro_data = ''

        self.assertRaises(ValueError, lambda: try_get_content_by_lang(test_micro_data, 'en'))

    def test_try_get_content_by_lang_must_return_nothing_when_dict_empty(self):
        from catalog.tools import try_get_content_by_lang

        test_micro_data = {}

        self.assertEqual('', try_get_content_by_lang(test_micro_data, 'en'))

    def test_try_get_content_by_lang_with_default_language(self):
        from catalog.tools import try_get_content_by_lang

        test_micro_data = {
            "pt": "Gerenciamento ... ",
            "it": "Gestione dei rifiuti sanitari in Izmir, Turchia"
        }

        content = try_get_content_by_lang(test_micro_data, 'en', 'it')

        self.assertEqual(content, 'Gestione dei rifiuti sanitari in Izmir, Turchia')

    def test_try_get_content_by_lang_without_languange_and_default_must_return_first_lang(self):
        from catalog.tools import try_get_content_by_lang

        test_micro_data = {
            "uk": "The United Kingdom of Great Britain and Northern Ireland",
            "pt-br": "Gestione dei rifiuti sanitari in Izmir, Turchia",
            "es": "Entonces yo estou aqui",
            "pt": "bla bla bla",
        }

        content = try_get_content_by_lang(test_micro_data, 'en', 'it')

        self.assertEqual(content, test_micro_data.get(test_micro_data.keys()[0]))
