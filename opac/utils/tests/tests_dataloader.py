import mocker


class MarretaDataLoaderTests(mocker.MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from utils.sync.dataloader import Marreta
        return Marreta(*args, **kwargs)

    def test_rebuild_database(self):
        mock_pymongo = self.mocker.mock()
        mock_mongo_conn = self.mocker.mock()
        mock_mongo_db = self.mocker.mock()
        mock_mongo_col = self.mocker.mock()

        mock_pymongo.Connection(host=mocker.ANY, port=mocker.ANY)
        self.mocker.result(mock_mongo_conn)

        mock_mongo_conn[mocker.ANY]
        self.mocker.result(mock_mongo_db)

        mock_mongo_db.drop_collection('journals')
        self.mocker.result(None)

        mock_mongo_db['journals']
        self.mocker.result(mock_mongo_col)

        mock_mongo_col.insert(
            {'title': "the hitchhiker's guide to the galaxy"}, w=1)
        self.mocker.result('spam_objectId')

        self.mocker.replay()

        m = self._makeOne(pymongo_dep=mock_pymongo)

        data = [{'title': "the hitchhiker's guide to the galaxy"}]
        self.assertIsNone(m.rebuild_collection('journals', data))

    def test_update_journals(self):
        mock_mongo_conn = self.mocker.mock()
        mock_mongo_db = self.mocker.mock()
        mock_mongo_col = self.mocker.mock()

        mock_mongo_conn(mongodb_driver=mocker.ANY, mongo_uri=mocker.ANY)
        self.mocker.result(mock_mongo_conn)

        mock_mongo_conn.db
        self.mocker.result(mock_mongo_db)

        mock_mongo_db['journals']
        self.mocker.result(mock_mongo_col)

        mock_mongo_col.update({'id': 1},
                              {
                                'title': "the hitchhiker's guide to the galaxy",
                                'id': 1,
                              },
                              w=1,
                              upsert=True)
        self.mocker.result('spam_objectId')

        self.mocker.replay()

        m = self._makeOne(mongoconn_dep=mock_mongo_conn)

        data = [{'title': "the hitchhiker's guide to the galaxy", 'id': 1}]
        self.assertIsNone(m.update_journals(data))

    def test_missing_settings_MONGO_URI_raises_exception(self):
        mock_settings = self.mocker.mock()

        mock_settings.MONGO_URI
        self.mocker.result(None)

        self.mocker.replay()

        self.assertRaises(ValueError,
            lambda: self._makeOne(settings=mock_settings))
