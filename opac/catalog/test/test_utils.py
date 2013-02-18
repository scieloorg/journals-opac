# coding: utf8
from collections import OrderedDict

from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)


class NavigationTest(MockerTestCase):

    def test_instatiation(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.utils import Navigation

        current_issue = {
                            u'id': 4,
                            u'order': 1,
                        }

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
        issue = IssueFactory.build(**current_issue)

        nav = Navigation(journal, issue)

        self.assertEqual(OrderedDict([(1, 4), (2, 5), (3, 6)]), nav._issues)

    def test_current_issue(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.utils import Navigation

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

        nav = Navigation(journal, issue).current_issue

        self.assertEqual(nav, '/issue/AISS/3/')

    def test_get_next_issue_id(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.utils import Navigation

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

        nav = Navigation(journal, issue).next_issue

        self.assertEqual(nav, '/issue/AISS/6/')

    def test_get_previous_issue_id(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.utils import Navigation

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

        nav = Navigation(journal, issue).previous_issue

        self.assertEqual(nav, '/issue/AISS/4/')

    def test_get_invalid_previous_issue_id_attemping_100_times(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.utils import Navigation

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

        nav = Navigation(journal, issue).previous_issue

        self.assertEqual(None, nav)

    def test_get_invalid_previous_issue_id_reaching_boundary_0(self):
        from .modelfactories import JournalFactory, IssueFactory
        from catalog.utils import Navigation

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

        nav = Navigation(journal, issue).previous_issue

        self.assertEqual(None, nav)
