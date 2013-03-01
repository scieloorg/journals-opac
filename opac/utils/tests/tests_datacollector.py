# coding: utf-8
import mocker

from catalog.test import modelfactories


class SciELOManagerAPITests(mocker.MockerTestCase):
    valid_full_microset = {
        'objects': [
            {
                'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
            },
        ],
        'meta': {'next': None},
    }
    valid_microset = {
        'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
    }

    def _makeOne(self, *args, **kwargs):
        from utils.sync.datacollector import SciELOManagerAPI
        return SciELOManagerAPI(*args, **kwargs)

    def test_fetching_all_docs_of_an_endpoint(self):
        mock_settings = self.mocker.mock()
        mock_slumber = self.mocker.mock()

        mock_settings.SCIELOMANAGER_API_URI
        self.mocker.result('http://manager.scielo.org/api/v1/')

        mock_settings.SCIELOMANAGER_API_USERNAME
        self.mocker.result('any.username')

        mock_settings.SCIELOMANAGER_API_KEY
        self.mocker.result('any.apikey')

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        mock_slumber.journals
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        api = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)

        res = api.fetch_data('journals')
        self.assertTrue('objects' in res)
        self.assertTrue(len(res['objects']), 1)

    def test_single_document_of_an_endpoint(self):
        mock_settings = self.mocker.mock()
        mock_slumber = self.mocker.mock()

        mock_settings.SCIELOMANAGER_API_URI
        self.mocker.result('http://manager.scielo.org/api/v1/')

        mock_settings.SCIELOMANAGER_API_USERNAME
        self.mocker.result('any.username')

        mock_settings.SCIELOMANAGER_API_KEY
        self.mocker.result('any.apikey')

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        mock_slumber.journals
        self.mocker.result(mock_slumber)

        mock_slumber(1)
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        api = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)

        res = api.fetch_data('journals', resource_id=1)
        self.assertIn('title', res)


class ChangesListTests(mocker.MockerTestCase):

    def test_raw_data_from_scielo_api_is_accepted_on_instantiation(self):
        from utils.sync.datacollector import ChangesList, Change

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

        ch_list = ChangesList(changes)

        for ch in ch_list._changes:
            self.assertIsInstance(ch, Change)

    def test_generate_another_changes_list_based_on_filtering_by_collections(self):
        from utils.sync.datacollector import ChangesList

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

        ch_list = ChangesList(changes)
        filtered_list = ch_list.filter(collections=[c])

        self.assertEqual(len(filtered_list._changes), 1)

    def test_generate_another_changes_list_based_on_filtering_by_journals(self):
        from utils.sync.datacollector import ChangesList

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

        ch_list = ChangesList(changes, list_issues_uri_dep=mocker_list_issues)
        filtered_list = ch_list.filter(journals=[j])

        self.assertEqual(len(filtered_list._changes), 1)

    def test_changeslist_is_iterable(self):
        from utils.sync.datacollector import ChangesList
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

        ch_list = ChangesList(changes)
        self.assertTrue(iter(ch_list))

    def test_changeslist_is_sorted_by_seq(self):
        from utils.sync.datacollector import ChangesList
        changes = [
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 9
            },
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/31/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            }
        ]

        ch_list = ChangesList(changes)
        self.assertEqual([ch.seq for ch in ch_list], [8, 9])
