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

    def setUp(self):
        self._catalog_pages_fixture = open(
            os.path.abspath(os.path.dirname(__file__)) + '/fixtures/catalog_pages.json',
            'r')
        self._catalog_journals_fixture = open(
            os.path.abspath(os.path.dirname(__file__)) + '/fixtures/catalog_journals.json',
            'r')
        self._catalog_issues_fixture = open(
            os.path.abspath(os.path.dirname(__file__)) + '/fixtures/catalog_issues.json',
            'r')
        self._invalid_json = open(
            os.path.abspath(os.path.dirname(__file__)) + '/fixtures/invalid.json',
            'r')

    def test_catalog_pages(self):
        from accesses import ratchet

        data = self._catalog_pages_fixture

        tab = ratchet.Accesses().catalog_pages(json_data=data)

        result = [
            [u'date', u'sci_abstract', u'sci_pdf', u'sci_arttext', u'download', u'sci_issuetoc', u'sci_issues', u'total'],
            [u'2011, Jan', 1743, 8684, 47328, 51095, 1710, 652, 111212],
            [u'2011, Feb', 3820, 8927, 46605, 55009, 1349, 417, 116127],
            [u'2012, Jan', 1741, 8682, 47326, 51093, 1708, 650, 111200],
            [u'2012, Feb', 3818, 8925, 46603, 55007, 1347, 415, 116115]
        ]

        self.assertEqual(tab[0], result[0])
        self.assertEqual(tab[1], result[1])
        self.assertEqual(tab[2], result[2])
        self.assertEqual(tab[3], result[3])
        self.assertEqual(tab[4], result[4])

    def test_catalog_pages_invalid_code(self):
        from accesses import ratchet

        data = self._invalid_json  # Invalid Json data or Empty results

        self.assertRaises(ValueError, lambda: ratchet.Accesses().catalog_pages(json_data=data))

    def test_catalog_journals(self):
        from accesses import ratchet

        data = self._catalog_journals_fixture

        tab = ratchet.Accesses().catalog_journals(json_data=data)

        result = [
            [u'journal', u'sci_abstract', u'sci_issuetoc', u'sci_issues', u'sci_pdf', u'sci_arttext', u'sci_serial', u'total'],
            [u'0102-311X', 3, 3, 3, 3, 3, 3, 18],
            [u'0034-8910', 4, 4, 4, 4, 4, 4, 24]
        ]

        self.assertEqual(tab[0], result[0])
        self.assertEqual(tab[1], result[1])
        self.assertEqual(tab[2], result[2])

    def test_catalog_issues(self):
        from accesses import ratchet

        data = self._catalog_issues_fixture

        tab = ratchet.Accesses().catalog_issues(json_data=data)

        result = [
            [u'journal', 'issue', 'accesses'],
            [u'0034-8910', u'0034-891019860005', 11],
            [u'0034-8910', u'0034-891019910001', 14]
        ]

        self.assertEqual(tab[0], result[0])
        self.assertEqual(tab[1], result[1])
        self.assertEqual(tab[2], result[2])

    def test_catalog_articles(self):
        from accesses import ratchet

        data = self._catalog_issues_fixture

        tab = ratchet.Accesses().catalog_articles(json_data=data)

        result = [
            [u'journal', 'issue', 'article', 'accesses'],
            [u'0034-8910', u'0034-891019860005', u'0034-891019860005', 11],
            [u'0034-8910', u'0034-891019910001', u'0034-891019910001', 14]
        ]

        self.assertEqual(tab[0], result[0])
        self.assertEqual(tab[1], result[1])
        self.assertEqual(tab[2], result[2])