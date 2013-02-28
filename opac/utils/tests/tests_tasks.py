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


class ChangesIdentificationTests(mocker.MockerTestCase, TestCase):

    def test_identify_journals_given_collections(self):
        from utils.tasks import identify_changes

        changes = [
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/31/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/issues/2840/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 9
            },
        ]

        c = modelfactories.CollectionMetaFactory.create()

        docs = identify_changes(changes, collections=[c], journals=[])

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0], "/api/v1/journals/31/")

    def test_identify_journals_given_journals(self):
        from utils.tasks import identify_changes

        mocker_list_issues = self.mocker.mock()
        mocker_list_issues(mocker.ANY)
        self.mocker.result([u'/api/v1/issues/1/'])
        self.mocker.replay()

        changes = [
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/31/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 9
            },
        ]

        j = modelfactories.JournalMetaFactory.create()

        docs = identify_changes(changes,
                                collections=[],
                                journals=[j],
                                list_issues_uri_dep=mocker_list_issues)

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0], "/api/v1/journals/1/")

    def test_identify_journals_given_journals_and_collections(self):
        from utils.tasks import identify_changes

        mocker_list_issues = self.mocker.mock()
        mocker_list_issues(mocker.ANY)
        self.mocker.result([u'/api/v1/issues/1/'])
        self.mocker.replay()

        changes = [
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/31/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 9
            },
            {
                "changed_at": "2013-01-23T15:13:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/2/",
                "resource_uri": "/api/v1/changes/3/",
                "seq": 10
            },
        ]

        c = modelfactories.CollectionMetaFactory.create(
            resource_uri="/api/v1/collections/2/"
        )
        c2 = modelfactories.CollectionMetaFactory.create(
            resource_uri="/api/v1/collections/1/"
        )
        j = modelfactories.JournalMetaFactory.create(
            collection=c,
            resource_uri="/api/v1/journals/1/"
        )

        docs = identify_changes(changes,
                                collections=[c2],
                                journals=[j],
                                list_issues_uri_dep=mocker_list_issues)

        self.assertEqual(len(docs), 2)
        self.assertIn("/api/v1/journals/31/", docs)
        self.assertIn("/api/v1/journals/1/", docs)

    def test_membership_is_irrelevant(self):
        from utils.tasks import identify_changes

        mocker_list_issues = self.mocker.mock()

        mocker_list_issues(mocker.ANY)
        self.mocker.result([u'/api/v1/issues/1/'])

        mocker_list_issues(mocker.ANY)
        self.mocker.result([])

        self.mocker.replay()

        changes = [
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/2/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 9
            },
        ]

        j = modelfactories.JournalMetaFactory.create(
            is_member=True,
            resource_uri=u'/api/v1/journals/1/')
        j2 = modelfactories.JournalMetaFactory.create(
            is_member=False,
            resource_uri=u'/api/v1/journals/2/')

        docs = identify_changes(changes,
                                collections=[],
                                journals=[j, j2],
                                list_issues_uri_dep=mocker_list_issues)

        self.assertEqual(len(docs), 2)

    def test_identify_issue_changes(self):
        from utils.tasks import identify_changes

        mocker_list_issues = self.mocker.mock()
        mocker_list_issues(mocker.ANY)
        self.mocker.result([u'/api/v1/issues/1/'])

        self.mocker.replay()

        journal_doc = modelfactories.JournalFactory.build()
        journal_meta = modelfactories.JournalMetaFactory.create()

        changes = [
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/2/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/issues/1/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 9
            },
        ]

        docs = identify_changes(changes,
                                collections=[],
                                journals=[journal_meta],
                                list_issues_uri_dep=mocker_list_issues)

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0], "/api/v1/issues/1/")
