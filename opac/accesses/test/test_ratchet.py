# encoding: utf-8
import os
import json

from mocker import (
    MockerTestCase,
    ANY,
    ARGS,
    KWARGS,
)


class RatchetTest(MockerTestCase):

    def test_catalog_pages(self):
        from accesses import ratchet

        data = json.loads(open(os.path.abspath(os.path.dirname(__file__))+'/fixtures/catalog.json', 'r').read())

        tab = ratchet.Accesses().catalog_pages(data=data)

        result = [
            [u'year', u'sci_abstract', u'sci_pdf', u'sci_arttext', u'download', u'sci_issuetoc', u'sci_issues'],
            [u'201201', 1741, 8682, 47326, 51093, 1708, 650],
            [u'201202', 3818, 8925, 46603, 55007, 1347, 415],
            [u'201102', 3820, 8927, 46605, 55009, 1349, 417],
            [u'201101', 1743, 8684, 47328, 51095, 1710, 652]]

        self.assertEqual(tab[0], result[0])
        self.assertEqual(tab[1], result[1])
        self.assertEqual(tab[2], result[2])
        self.assertEqual(tab[3], result[3])
        self.assertEqual(tab[4], result[4])