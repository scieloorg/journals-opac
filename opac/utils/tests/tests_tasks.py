# coding: utf-8
import mocker

from django.test import TestCase

from catalog import models
from catalog.test import modelfactories
from utils.tasks import (
    _what_to_sync,
    sync_collections_meta,
    sync_journals_meta,
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

        to_sync = list(_what_to_sync(managerapi_dep=mocker_scieloapi))

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

        to_sync = list(_what_to_sync(managerapi_dep=mocker_scieloapi))

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

        to_sync = list(_what_to_sync(managerapi_dep=mocker_scieloapi))

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

        to_sync = list(_what_to_sync(managerapi_dep=mocker_scieloapi))

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

        to_sync = list(_what_to_sync(managerapi_dep=mocker_scieloapi))

        self.assertEqual(len(to_sync), 0)


class SyncCollectionsMetaTests(mocker.MockerTestCase, TestCase):

    def test_data_is_loaded_if_all_goes_fine(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_collections()
        self.mocker.result([
            {
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
            }
        ])

        self.mocker.replay()

        sync_collections_meta(managerapi_dep=mocker_scieloapi)

        self.assertEqual(models.CollectionMeta.objects.count(), 1)

    def test_default_value_for_is_member_equals_False(self):
        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_collections()
        self.mocker.result([
            {
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
            }
        ])

        self.mocker.replay()

        sync_collections_meta(managerapi_dep=mocker_scieloapi)

        self.assertFalse(models.CollectionMeta.objects.get(name_slug=u'saude-publica').is_member)

    def test_is_member_attribute_must_resist_on_syncs(self):

        modelfactories.CollectionMetaFactory.create(**{
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
                'is_member': True,
            })

        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_collections()
        self.mocker.result([
            {
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
            }
        ])

        self.mocker.replay()

        sync_collections_meta(managerapi_dep=mocker_scieloapi)

        self.assertTrue(models.CollectionMeta.objects.get(name_slug=u'saude-publica').is_member)

    def test_Resource_uri_Rame_and_Name_slug_attrs_must_match_on_updates(self):
        modelfactories.CollectionMetaFactory.create(**{
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
                'is_member': True,
            })

        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_collections()
        self.mocker.result([
            {
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Privada',
                'name_slug': u'saude-privada',
            }
        ])

        self.mocker.replay()

        sync_collections_meta(managerapi_dep=mocker_scieloapi)

        self.assertEqual(models.CollectionMeta.objects.count(), 2)


class SyncJournalsMetaTests(mocker.MockerTestCase, TestCase):

    def test_data_is_loaded_if_all_goes_fine(self):
        modelfactories.CollectionMetaFactory.create(**{
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
                'is_member': True,
            })

        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals(u'saude-publica')
        self.mocker.result([
            {
                'resource_uri': u'/api/v1/journals/1/',
                'title': u"Annali dell'Istituto Superiore di Sanit\xe0",
                'collections': u'/api/v1/collections/1/',
            }
        ])

        self.mocker.replay()

        sync_journals_meta(managerapi_dep=mocker_scieloapi)

        self.assertEqual(models.JournalMeta.objects.count(), 1)

    def test_bypass_journals_with_non_member_collections(self):
        modelfactories.CollectionMetaFactory.create(**{
                'resource_uri': u'/api/v1/collections/1/',
                'name': u'Saúde Pública',
                'name_slug': u'saude-publica',
                'is_member': False,
            })

        mocker_scieloapi = self.mocker.mock()

        mocker_scieloapi(settings=mocker.ANY)
        self.mocker.result(mocker_scieloapi)

        mocker_scieloapi.get_all_journals()
        self.mocker.result([])

        self.mocker.replay()

        sync_journals_meta(managerapi_dep=mocker_scieloapi)

        self.assertEqual(models.JournalMeta.objects.count(), 0)
