# coding: utf-8
import mocker
from django.test import TestCase
from django.utils import timezone

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


class MakeJournalPipelineTests(TestCase):

    def test_returns_a_pipeline_instance(self):
        from utils.functions import make_journal_pipeline
        from utils.sync.pipes import Pipeline

        ppl = make_journal_pipeline()
        self.assertIsInstance(ppl, Pipeline)


class GetAllChangesTests(mocker.MockerTestCase, TestCase):

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

    def test_all_colaborating_objects_are_called(self):
        from utils.functions import get_all_changes
        from utils.sync.datacollector import ChangesList

        mock_manager_api = self.mocker.mock()
        mock_catalog_defs = self.mocker.mock()
        mock_changeslist = self.mocker.mock(ChangesList)

        mock_manager_api(settings=mocker.ANY)
        self.mocker.result(mock_manager_api)

        mock_catalog_defs()
        self.mocker.result(([], []))

        mock_manager_api.get_changes(since=mocker.ANY)
        self.mocker.result(self.changes)

        mock_changeslist(self.changes)
        self.mocker.result(mock_changeslist)

        mock_changeslist.filter(collections=[], journals=[])
        self.mocker.result(mock_changeslist)

        self.mocker.replay()

        changes = get_all_changes(managerapi_dep=mock_manager_api,
                                  catalog_defs_dep=mock_catalog_defs,
                                  changeslist_dep=mock_changeslist)

        self.assertIsInstance(changes, ChangesList)


class ListIssuesURITests(mocker.MockerTestCase, TestCase):

    def test_a_list_of_issue_uris_is_returned(self):
        from utils.functions import _list_issues_uri

        mock_journal = self.mocker.mock()
        mock_journalmeta = self.mocker.mock()
        mock_issue = self.mocker.mock()

        mock_journalmeta.resource_id
        self.mocker.result(1)

        mock_journal.get_journal(criteria={'id': 1})
        self.mocker.result(mock_journal)

        mock_journal.list_issues()
        self.mocker.result([mock_issue])

        mock_issue.resource_uri
        self.mocker.result('/api/v1/issues/2840/')

        self.mocker.replay()

        issues = _list_issues_uri(mock_journalmeta, journal_dep=mock_journal)
        self.assertEqual(list(issues), ['/api/v1/issues/2840/'])


class GetLastSeqTests(mocker.MockerTestCase, TestCase):

    def test_last_seq_is_returned_when_sync_exists(self):
        from utils.functions import get_last_seq

        sync = modelfactories.SyncFactory.create()

        self.assertEqual(sync.last_seq, get_last_seq())

    def test_zero_seq_is_returned_when_sync_dont_exists(self):
        from utils.functions import get_last_seq

        self.assertEqual(0, get_last_seq())

    def test_lastest_sync_is_used(self):
        from utils.functions import get_last_seq

        sync = modelfactories.SyncFactory.create(last_seq=2,
            ended_at=timezone.now())
        sync2 = modelfactories.SyncFactory.create(last_seq=3,
            ended_at=timezone.now())

        self.assertEqual(sync2.last_seq, get_last_seq())


class GetRemoteLastSeq(mocker.MockerTestCase, TestCase):

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

    changes2 = [
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
        },
    ]

    def test_all_colaborating_objects_are_called(self):
        from utils.functions import get_remote_last_seq

        mock_managerapi = self.mocker.mock()

        mock_managerapi(settings=mocker.ANY)
        self.mocker.result(mock_managerapi)

        mock_managerapi.get_changes()
        self.mocker.result(self.changes)

        self.mocker.replay()

        self.assertEqual(9, get_remote_last_seq(managerapi_dep=mock_managerapi))

    def test_zero_is_returned_if_seq_attribute_is_missing(self):
        from utils.functions import get_remote_last_seq

        mock_managerapi = self.mocker.mock()

        mock_managerapi(settings=mocker.ANY)
        self.mocker.result(mock_managerapi)

        mock_managerapi.get_changes()
        self.mocker.result(self.changes2)

        self.mocker.replay()

        self.assertEqual(0, get_remote_last_seq(managerapi_dep=mock_managerapi))
