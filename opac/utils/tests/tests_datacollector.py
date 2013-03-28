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

    def test_fetching_all_docs_of_an_endpoint_retries_after_connection_error(self):
        import requests

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
        self.mocker.throw(requests.exceptions.ConnectionError)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        api = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)

        res = api.fetch_data('journals')
        self.assertTrue('objects' in res)
        self.assertTrue(len(res['objects']), 1)

    def test_fetching_all_docs_of_an_endpoint_raises_exception_after_attempts_are_exhausted(self):
        import requests
        from utils.sync.datacollector import ResourceUnavailableError

        mock_settings = self.mocker.mock()
        mock_slumber = self.mocker.mock()
        mock_time = self.mocker.mock()

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
        self.mocker.throw(requests.exceptions.ConnectionError)
        self.mocker.count(11)

        mock_time.sleep(mocker.ANY)
        self.mocker.result(None)
        self.mocker.count(10)

        self.mocker.replay()

        api = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)

        self.assertRaises(ResourceUnavailableError,
            lambda: api.fetch_data('journals', time_dep=mock_time))

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

    def test_missing_settings_SCIELOMANAGER_API_URI_raises_exception(self):
        mock_settings = self.mocker.mock()

        mock_settings.SCIELOMANAGER_API_URI
        self.mocker.result(None)

        mock_settings.SCIELOMANAGER_API_KEY
        self.mocker.result('foo')

        mock_settings.SCIELOMANAGER_API_USERNAME
        self.mocker.result('foo')

        self.mocker.replay()

        self.assertRaises(ValueError,
            lambda: self._makeOne(settings=mock_settings))

    def test_missing_settings_SCIELOMANAGER_API_KEY_raises_exception(self):
        mock_settings = self.mocker.mock()

        mock_settings.SCIELOMANAGER_API_URI
        self.mocker.result('foo')

        mock_settings.SCIELOMANAGER_API_KEY
        self.mocker.result(None)

        mock_settings.SCIELOMANAGER_API_USERNAME
        self.mocker.result('foo')

        self.mocker.replay()

        self.assertRaises(ValueError,
            lambda: self._makeOne(settings=mock_settings))

    def test_missing_settings_SCIELOMANAGER_API_USERNAME_raises_exception(self):
        mock_settings = self.mocker.mock()

        mock_settings.SCIELOMANAGER_API_URI
        self.mocker.result('foo')

        mock_settings.SCIELOMANAGER_API_KEY
        self.mocker.result('foo')

        mock_settings.SCIELOMANAGER_API_USERNAME
        self.mocker.result(None)

        self.mocker.replay()

        self.assertRaises(ValueError,
            lambda: self._makeOne(settings=mock_settings))

    def test_iter_docs_returns_a_generator(self):
        import types
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber)
        self.assertIsInstance(sapi.iter_docs('journals'), types.GeneratorType)

    def test_iter_docs_makes_seamless_pagination(self):
        valid_full_microset1 = {
            'objects': [
                {
                    'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
                },
            ],
            'meta': {'next': '/api/v1/journals/?some_values'},
        }
        valid_full_microset2 = {
            'objects': [
                {
                    'title': u'EFGH. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
                },
            ],
            'meta': {'next': None},
        }

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
        self.mocker.count(2)

        mock_slumber.get(api_key='any.apikey', username='any.username', limit=50, offset=0)
        self.mocker.result(valid_full_microset1)

        mock_slumber.get(api_key='any.apikey', username='any.username', limit=50, offset=50)
        self.mocker.result(valid_full_microset2)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)
        for i, doc in enumerate(sapi.iter_docs('journals')):
            if i == 0:
                self.assertTrue(doc['title'].startswith('ABCD'))
            else:
                self.assertTrue(doc['title'].startswith('EFGH'))

    def test_iter_docs_ignores_trashed_docs(self):
        valid_full_microset1 = {
            'objects': [
                {
                    'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
                },
                {
                    'title': u'EFGH. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
                    'is_trashed': True,
                },
            ],
            'meta': {'next': None},
        }

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

        mock_slumber.get(api_key='any.apikey', username='any.username', limit=50, offset=0)
        self.mocker.result(valid_full_microset1)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)
        self.assertEqual(1, len(list(sapi.iter_docs('journals'))))

    def test_iter_docs_accepts_filter_by_collection(self):
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

        mock_slumber.get(api_key='any.apikey',
                         username='any.username',
                         limit=50,
                         offset=0,
                         collection='saude-publica')
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)
        self.assertEqual(1, len(list(sapi.iter_docs('journals', collection='saude-publica'))))

    def test_get_all_journals_from_collection(self):
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

        mock_slumber.get(api_key='any.apikey',
                         username='any.username',
                         limit=50,
                         offset=0,
                         collection='saude-publica')
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)
        self.assertEqual(1, len(list(sapi.get_all_journals('saude-publica'))))

    def test_get_journals_from_resource_ids(self):
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

        mock_slumber(47)
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_full_microset)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)
        self.assertEqual(1, len(list(sapi.get_journals(47))))

    def test_get_all_collections_returns_a_generator(self):
        import types
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber)
        self.assertIsInstance(sapi.get_all_collections(), types.GeneratorType)

    def test_get_changes_returns_a_generator(self):
        import types
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber)
        self.assertIsInstance(sapi.get_changes(), types.GeneratorType)

    def test_get_issues_returns_a_generator(self):
        import types
        mock_slumber = self.mocker.mock()

        mock_slumber.API('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_slumber)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber)
        self.assertIsInstance(sapi.get_issues(), types.GeneratorType)

    def test_get_issues_from_resource_ids(self):
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

        mock_slumber.issues
        self.mocker.result(mock_slumber)

        mock_slumber(47)
        self.mocker.result(mock_slumber)

        mock_slumber.get(api_key='any.apikey', username='any.username')
        self.mocker.result(self.valid_microset)

        self.mocker.replay()

        sapi = self._makeOne(slumber_lib=mock_slumber, settings=mock_settings)
        self.assertEqual(1, len(list(sapi.get_issues(47))))


class ChangesListTests(mocker.MockerTestCase):

    def test_type_is_checked_at_instantiation(self):
        from utils.sync.datacollector import ChangesList
        self.assertRaises(TypeError, lambda: ChangesList('must fail'))

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

    def test_get_current_seq_while_iterating(self):
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
        i_ch_list = iter(ch_list)

        i_ch_list.next()
        self.assertEqual(i_ch_list.current_seq, 8)

        i_ch_list.next()
        self.assertEqual(i_ch_list.current_seq, 9)

    def test_get_current_seq_on_a_non_primed_iterator_raises_attribute_error(self):
        """
        To prime an iterator means to call its ``next`` method at
        least once.
        """
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
        i_ch_list = iter(ch_list)
        self.assertRaises(AttributeError, lambda: i_ch_list.current_seq)

    def test_show_only_changes_on_some_endpoints(self):
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
                "object_uri": "/api/v1/issues/31/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 8
            }
        ]

        ch_list = ChangesList(changes)
        for ch in ch_list.show('journals'):
            self.assertTrue('journals' in ch.object_uri)

    def test_show_unique_changes_on_some_endpoints(self):
        from utils.sync.datacollector import ChangesList
        changes = [
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/1/",
                "seq": 1
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/2/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 2
            },
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 3
            }
        ]

        ch_list = ChangesList(changes)
        i_ch_list = ch_list.show('journals', unique=True)
        changes = list(i_ch_list)

        self.assertTrue(len(changes), 2)
        self.assertEqual(changes[0].seq, 2)
        self.assertEqual(changes[1].seq, 3)

    def test_unique_records_from_different_endpoints_doesnt_clash(self):
        from utils.sync.datacollector import ChangesList
        changes = [
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/1/",
                "seq": 1
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/2/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 2
            },
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 3
            },
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/issues/1/",
                "resource_uri": "/api/v1/changes/9/",
                "seq": 4
            }
        ]

        ch_list = ChangesList(changes)
        i_ch_list = ch_list.show('journals', unique=True)
        changes = list(i_ch_list)

        self.assertTrue(len(changes), 2)
        self.assertEqual(changes[0].seq, 2)
        self.assertEqual(changes[1].seq, 3)

    def test_last_seq(self):
        from utils.sync.datacollector import ChangesList
        changes = [
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/1/",
                "seq": 1
            },
            {
                "changed_at": "2013-01-23T15:12:33.409478",
                "collection_uri": "/api/v1/collections/2/",
                "event_type": "added",
                "object_uri": "/api/v1/journals/2/",
                "resource_uri": "/api/v1/changes/2/",
                "seq": 2
            },
            {
                "changed_at": "2013-01-23T15:11:33.409478",
                "collection_uri": "/api/v1/collections/1/",
                "event_type": "updated",
                "object_uri": "/api/v1/journals/1/",
                "resource_uri": "/api/v1/changes/8/",
                "seq": 3
            }
        ]

        ch_list = ChangesList(changes)
        self.assertEqual(ch_list.last_seq, 3)


class ChangesListIteratorTests(mocker.MockerTestCase):

    changes = [
        {
            "changed_at": "2013-01-23T15:12:33.409478",
            "collection_uri": "/api/v1/collections/2/",
            "event_type": "added",
            "object_uri": "/api/v1/journals/1/",
            "resource_uri": "/api/v1/changes/1/",
            "seq": 1
        },
        {
            "changed_at": "2013-01-23T15:12:33.409478",
            "collection_uri": "/api/v1/collections/2/",
            "event_type": "added",
            "object_uri": "/api/v1/journals/2/",
            "resource_uri": "/api/v1/changes/2/",
            "seq": 2
        },
        {
            "changed_at": "2013-01-23T15:11:33.409478",
            "collection_uri": "/api/v1/collections/1/",
            "event_type": "updated",
            "object_uri": "/api/v1/journals/1/",
            "resource_uri": "/api/v1/changes/8/",
            "seq": 3
        },
        {
            "changed_at": "2013-01-23T15:11:33.409478",
            "collection_uri": "/api/v1/collections/1/",
            "event_type": "updated",
            "object_uri": "/api/v1/issues/1/",
            "resource_uri": "/api/v1/changes/9/",
            "seq": 4
        }
    ]

    def _makeOne(self):
        from utils.sync.datacollector import ChangesList
        return iter(ChangesList(self.changes))

    def test_iter_is_implemented_and_returns_self(self):
        chlist_iterator = self._makeOne()
        chlist_iterator2 = iter(chlist_iterator)
        self.assertIs(chlist_iterator, chlist_iterator2)

    def test_current_seq_raises_exception_for_non_started_iterators(self):
        chlist_iterator = self._makeOne()

        self.assertRaises(AttributeError, lambda: chlist_iterator.current_seq)


class ListIssuesUriTests(mocker.MockerTestCase):

    def test_list_issues_given_a_journalmeta(self):
        from utils.sync.datacollector import _list_issues_uri

        journal_meta = modelfactories.JournalMetaFactory.create()
        journal_doc = modelfactories.JournalFactory.build()

        mock_journal = self.mocker.mock()

        mock_journal.get_journal({'id': '1'})
        self.mocker.result(journal_doc)

        self.mocker.replay()

        issues = _list_issues_uri(journal_meta, journal_dep=mock_journal)
        issues_list = list(issues)
        self.assertEqual(len(issues_list), 1)
        self.assertEqual(issues_list[0], u'/api/v1/issues/1/')
