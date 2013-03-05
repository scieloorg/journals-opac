# coding: utf-8
import mocker

from django.test import TestCase

from catalog.test import modelfactories
from utils.functions import (
    get_all_data_for_build,
)


class WhatToSyncTests(mocker.MockerTestCase, TestCase):

    def test_sync_entire_collection_if_journals_are_not_specified(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals(u'saude-publica')
        self.mocker.result([{'acronym': 'aiss'}])

        mocker_scieloapi.get_journals(*[])
        self.mocker.result([])

        self.mocker.replay()

        c = modelfactories.CollectionMetaFactory.create(is_member=True)
        modelfactories.JournalMetaFactory.create(is_member=False, collection=c)

        to_sync = list(get_all_data_for_build(managerapi_dep=mocker_scieloapi))

        self.assertEqual(len(to_sync), 1)
        self.assertEqual(to_sync[0], {'acronym': 'aiss'})

    def test_sync_detached_journals_if_they_are_specified(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals(*[])
        self.mocker.result([])

        mocker_scieloapi.get_journals(u'1')
        self.mocker.result([{'acronym': 'aiss'}])

        self.mocker.replay()

        c = modelfactories.CollectionMetaFactory.create(is_member=True)
        modelfactories.JournalMetaFactory.create(is_member=True, collection=c)
        modelfactories.JournalMetaFactory.create(is_member=False, collection=c)

        to_sync = list(get_all_data_for_build(managerapi_dep=mocker_scieloapi))

        self.assertEqual(len(to_sync), 1)
        self.assertEqual(to_sync[0], {'acronym': 'aiss'})

    def test_sync_many_detached_journals_if_they_are_specified(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals(*[])
        self.mocker.result([])

        mocker_scieloapi.get_journals(u'1', u'1')
        self.mocker.result([{'acronym': 'aiss'}, {'acronym': 'aiss'}])

        self.mocker.replay()

        c = modelfactories.CollectionMetaFactory.create(is_member=True)
        modelfactories.JournalMetaFactory.create(is_member=True, collection=c)
        modelfactories.JournalMetaFactory.create(is_member=True, collection=c)

        to_sync = list(get_all_data_for_build(managerapi_dep=mocker_scieloapi))

        self.assertEqual(len(to_sync), 2)
        self.assertEqual(to_sync[0], {'acronym': 'aiss'})
        self.assertEqual(to_sync[1], {'acronym': 'aiss'})

    def test_sync_nothing_if_nothing_is_specified(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals(*[])
        self.mocker.result([])

        mocker_scieloapi.get_journals(*[])
        self.mocker.result([])

        self.mocker.replay()

        c = modelfactories.CollectionMetaFactory.create(is_member=False)
        modelfactories.JournalMetaFactory.create(is_member=False, collection=c)
        modelfactories.JournalMetaFactory.create(is_member=False, collection=c)

        to_sync = list(get_all_data_for_build(managerapi_dep=mocker_scieloapi))

        self.assertEqual(len(to_sync), 0)

    def test_ignore_journals_marked_as_members_if_the_journal_is_not(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals(*[])
        self.mocker.result([])

        mocker_scieloapi.get_journals(*[])
        self.mocker.result([])

        self.mocker.replay()

        c = modelfactories.CollectionMetaFactory.create(is_member=False)
        modelfactories.JournalMetaFactory.create(is_member=True, collection=c)

        to_sync = list(get_all_data_for_build(managerapi_dep=mocker_scieloapi))

        self.assertEqual(len(to_sync), 0)
