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

        mock_mongomanager.sort('_normalized_title', direction=pymongo.ASCENDING)
        self.mocker.result([{'title': 'Micronucleated'}])

        self.mocker.replay()

        journals = list_journals(mongomanager_lib=mock_mongomanager)

        self.assertEqual(catalog.journal_alpha_list(journals),
            '<ul class="unstyled"><li><a href="#">Micronucleated</a> - 0 issues</li></ul>')

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

        mock_mongomanager.sort('_normalized_title', direction=pymongo.ASCENDING)
        self.mocker.result([{'title': 'Micronucleated'}])
        self.mocker.count(1)

        self.mocker.replay()

        journals = list_journals_by_study_areas(mongomanager_lib=mock_mongomanager)

        self.assertEqual(catalog.journals_by_subject(journals),
            '<dl><dt>ZAP</dt><dd><dl><dd><ul class="unstyled"><li><a href="#">Micronucleated</a> - 0 issues</li></ul></dd></dl></dd></dl>')

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
            '<ul class="unstyled"><li><a href="#">Zap</a></li><li><a href="#">Zaz</a></li><li><a href="#">Spam</a></li></ul>')
