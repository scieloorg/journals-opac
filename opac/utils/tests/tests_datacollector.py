# coding: utf-8
import mocker


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
