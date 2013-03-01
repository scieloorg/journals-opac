# encoding: utf-8
import unittest

from django.test import TestCase
from django.test.utils import override_settings

import pymongo
from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)


class RatchetTemplateTagTest(MockerTestCase, TestCase):

    @override_settings(DEBUG=True, RATCHET_URI='http://localhost:8860/api/v1/')
    def test_ratchet_caller_debug_environment(self):
        from catalog.templatetags import catalogtags

        issue_access = {
                    'resource': 'issue',
                    'code': 1,
                    'journal': 1,
                    }
        caller = catalogtags.ratchet_caller(**issue_access)

        self.assertEqual(caller, '')

    @override_settings(DEBUG=False, RATCHET_URI='http://localhost:8860/api/v1/')
    def test_ratchet_caller_issue_access(self):
        from catalog.templatetags import catalogtags

        issue_access = {
                    'resource': 'issue',
                    'code': 1,
                    'journal': 1,
                    }

        caller = catalogtags.ratchet_caller(**issue_access)

        self.assertEqual(caller, 'ratchet_obj = {"journal": 1, "code": 1, "resource": "issue", "ratchet_uri": "http://localhost:8860/api/v1/"}; send_access(ratchet_obj);')

    @override_settings(DEBUG=False, RATCHET_URI='http://localhost:8860/api/v1/')
    def test_ratchet_caller_journal_access(self):
        from catalog.templatetags import catalogtags

        issue_access = {
                    'resource': 'journal',
                    'code': 1,
                    }

        caller = catalogtags.ratchet_caller(**issue_access)

        self.assertEqual(caller, 'ratchet_obj = {"code": 1, "resource": "journal", "ratchet_uri": "http://localhost:8860/api/v1/"}; send_access(ratchet_obj);')


class IssueTemplateTagTest(MockerTestCase, TestCase):

    @unittest.expectedFailure
    def test_list_articles_by_section(self):
        from catalog.templatetags import catalogtags
        from catalog.mongomodels import Issue
        from catalog.mongomodels import Section
        from catalog.mongomodels import Article

        issue_mock_objects = self.mocker.mock()
        section_mock_objects = self.mocker.mock()
        article_mock_objects = self.mocker.mock()

        issue_section_microdata = {
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
            'abstract': {
                'en': "<p>Trout farming, that represents the most important sector for aquaculture inland production in Italy, ...",
                'it': "<p>La troticoltura rappresenta il settore più importante per la produzione ittica in Italia ed è in grado ..."
              },
            'title': 'Micronucleated lymphocytes in parents of lalala children',
            'title_group': {
                'en': 'Management of health-care waste in Izmir, Turkey',
            'it': 'Gestione dei rifiuti sanitari in Izmir, Turchia'
            },
            'contrib_group': {
                'author': [
                    {
                        'role': 'ND',
                        'given_names': 'Ahmet',
                        'surname': 'Soysal',
                        'affiliations': [
                        'A01'
                        ]
                    }]
            },
        }

        issue_mock_objects.find_one({'id': 1, 'issues.id': 1}, {'issues.data': 1})
        self.mocker.result(issue_section_microdata)

        section_mock_objects.find_one({'id': 1, 'sections.id': 514}, {'sections.data': 1})
        self.mocker.result(section_microdata)

        article_mock_objects.find_one({'id': 'AISS-JHjashA'})
        self.mocker.result(article_microdata)

        self.mocker.replay()

        Issue.objects = issue_mock_objects
        Section.objects = section_mock_objects
        Article.objects = article_mock_objects

        issue = Issue.get_issue(journal_id=1, issue_id=1)

        sections = issue.list_sections()

        self.assertEqual(catalogtags.list_articles_by_section(sections, 'en'), '<dl class="issue_toc"><dt><i class="icon-chevron-right"></i> WHO Publications</dt><dd><ul class="unstyled toc_article"><li>Management of health-care waste in Izmir, Turkey<ul class="inline toc_article_authors"><li><a href="#">Soysal, Ahmet</a>;</li></ul><ul class="inline toc_article_links"><li>abstract: <a href="#">en</a>  | <a href="#">it</a> </li></ul></li></dl>')
