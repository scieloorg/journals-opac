# encoding: utf-8
from collections import OrderedDict

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
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 3,
                    u'id': 6,
                },
            },
            {
                u'id': 5,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 2,
                    u'id': 5,
                },
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build()

        nav = Navigation(journal, issue=issue)

        self.assertEqual(nav._issues, OrderedDict([(1, 4), (2, 5), (3, 6)]))
        self.assertEqual(nav._current, 6)
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
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 3,
                    u'id': 6,
                },
            },
            {
                u'id': 5,
                u'data':
                {
                    u'total_documents': 3,
                    u'order': 2,
                    u'id': 5,
                },
            }
        ]

        issue = IssueFactory.build()
        mock_issue.get_issue(ANY, ANY)
        self.mocker.result(issue)
        self.mocker.replay()

        journal = JournalFactory.build(issues=issues)

        nav = Navigation(journal, issue_lib=mock_issue)

        self.assertEqual(nav._issues, OrderedDict([(1, 4), (2, 5), (3, 6)]))
        self.assertEqual(nav._current, 6)
        self.assertEqual(nav._issue, issue)

    def test_journal_with_ahead(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        journal_data = {
                            u'current_ahead_documents': 10,
                        }

        journal = JournalFactory.build(**journal_data)
        issue = IssueFactory()

        nav = Navigation(journal, issue).ahead

        self.assertEqual(nav, '/ahead/AISS/')

    def test_journal_without_ahead(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        journal = JournalFactory.build()
        issue = IssueFactory()

        nav = Navigation(journal, issue=issue).ahead

        self.assertEqual(nav, None)

    def test_current_issue(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 1,
                            u'id': 4,
                        }

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
                    }
                }
            ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).current_issue

        self.assertEqual(nav, '/issue/AISS/3/')

    def test_get_next_issue_id(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 1,
                            u'id': 4,
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 1,
                    u'id': 4,
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'order': 3,
                    u'id': 6,
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
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 1,
                    u'id': 4,
                },
            },
            {
                u'id': 6,
                u'data':
                {
                    u'order': 3,
                    u'id': 6,
                },
            }
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).previous_issue

        self.assertEqual(nav, '/issue/AISS/4/')

    def test_get_invalid_previous_issue_id_attemping_100_times(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 101,
                            u'id': 20,
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 1,
                    u'id': 4,
                },
            },
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).previous_issue

        self.assertEqual(None, nav)

    def test_get_invalid_previous_issue_id_reaching_boundary_0(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.tools import Navigation

        current_issue = {
                            u'order': 10,
                            u'id': 20,
                        }

        issues = [
            {
                u'id': 4,
                u'data':
                {
                    u'order': 100,
                    u'id': 4,
                },
            },
        ]

        journal = JournalFactory.build(issues=issues)
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue=issue).previous_issue

        self.assertEqual(None, nav)
