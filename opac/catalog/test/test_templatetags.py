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


class JournalTemplateTagTest(TestCase, MockerTestCase):

    def test_journal_alpha_list(self):
        from catalog.templatetags import catalog
        from catalog.mongomodels import list_journals

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.find({})
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.sort('title', direction=pymongo.ASCENDING)
        self.mocker.result([{'title': 'Micronucleated'}])

        self.mocker.replay()

        journals = list_journals(mongomanager_lib=mock_mongomanager)

        self.assertEqual(catalog.journal_alpha_list(journals),
            u'<ul class="unstyled"><li><a href="#">Micronucleated</a> - 0 issues</li></ul>')

    def test_journal_by_subject(self):
        from catalog.templatetags import catalog
        from catalog.mongomodels import list_journals_by_study_areas

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)
        self.mocker.count(2)

        mock_mongomanager.distinct('study_areas')
        self.mocker.result(['Zap'])

        mock_mongomanager.find({'study_areas': 'Zap'})
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.sort('title', direction=pymongo.ASCENDING)
        self.mocker.result([{'title': 'Micronucleated'}])
        self.mocker.count(1)

        self.mocker.replay()

        journals = list_journals_by_study_areas(mongomanager_lib=mock_mongomanager)

        self.assertEqual(catalog.journals_by_subject(journals),
            u'<dl><dt>ZAP</dt><dd><dl><dd><ul class="unstyled"><li><a href="#">Micronucleated</a> - 0 issues</li></ul></dd></dl></dd></dl>')

    def test_subject_list(self):
        from catalog.templatetags import catalog
        from catalog.mongomodels import list_journals_by_study_areas

        mock_mongomanager = self.mocker.mock()

        mock_mongomanager(mongo_collection='journals')
        self.mocker.result(mock_mongomanager)

        mock_mongomanager.distinct('study_areas')
        self.mocker.result(['Zap', 'Zaz', 'Spam'])

        self.mocker.replay()

        journals = list_journals_by_study_areas(mongomanager_lib=mock_mongomanager)
        self.assertEqual(catalog.subject_list(journals),
            u'<ul class="unstyled"><li><a href="#">Zap</a></li><li><a href="#">Zaz</a></li><li><a href="#">Spam</a></li></ul>')


class IssueTemplateTagTest(TestCase, MockerTestCase):

    def test_issues_list_with_articles(self):
        from catalog.templatetags import catalog
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

        self.assertEqual(catalog.issues_list_with_articles(sections, 'en'), '<dl class="issue_toc"><dt><i class="icon-chevron-right"></i> WHO Publications</dt><dd><ul class="unstyled toc_article"><li>Management of health-care waste in Izmir, Turkey<ul class="inline toc_article_authors"><li><a href="#">Soysal, Ahmet</a>;</li></ul><ul class="inline toc_article_links"><li>abstract: <a href="#">en</a>  | <a href="#">it</a> </li></ul></li></dl>')
