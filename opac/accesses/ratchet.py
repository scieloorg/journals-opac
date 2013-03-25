import urllib2
import json
import copy

from collections import OrderedDict

from django.conf import settings

async_mongo_limit = 1000000


class Accesses(object):

    def __init__(self, ratchet_uri=settings.RATCHET_URI, resource='general'):
        self._ratchet = '{0}{1}'.format(ratchet_uri, resource)

    def catalog_pages(self,
                      json_data=None,
                      code=settings.RATCHET_CATALOG_CODE,
                      limit=async_mongo_limit):
        """
        Recover general access log from the catalog.
        Pages as Label
        Year-Month as X-axis
        accesses as Y-axis

        """
        req = '{0}?code={1}&limit{2}'.format(self._ratchet, code, limit)

        if json_data:
            raw_data = json_data.read()
        else:
            raw_data = urllib2.urlopen(req).read()

        data = json.loads(raw_data)[0]

        del data['total']
        del data['code']

        tab = {}
        tab['columns'] = []
        tab['rows'] = {}
        for key, value in data.items():
            if key[0] == 'y':
                del data[key]
            else:
                del value['total']
                tab['columns'].append(key)
                for year, months in value.items():
                    del months['total']
                    for month, days in months.items():
                        dat = u'{0}-{1}'.format(year[1:], month[1:])
                        l = tab['rows'].setdefault(dat, [])
                        l.append(days['total'])

        rows = []
        rows.append([u'date'] + tab['columns'] + [u'total'])
        for key, values in OrderedDict(sorted(tab['rows'].items())).items():
            row = []
            row.append(key)
            total = 0
            for value in values:
                total += value
                row.append(value)
            row.append(total)

            rows.append(row)

        return rows

    def catalog_journals(self,
                         json_data=None,
                         code=None,
                         doc_type=None,
                         limit=async_mongo_limit):
        """
        Recover general journals access log from the catalog.
        """

        if json_data:
            raw_data = json_data.read()
        else:
            query = u"code={0}".format(code)
            if doc_type:
                query = u"type={0}".format(doc_type)

            raw_data = urllib2.urlopen('{0}?{1}&limit={2}'.format(
                self._ratchet,
                query,
                limit))

        data = json.loads(raw_data)

        rows = []
        columns = [u'journal']

        for item in data:
            row = []
            issn = item['code']
            total = item['total']
            del item['code']
            del item['type']
            del item['total']
            del item['journal']

            row.append(issn)
            for key, value in item.items():
                if not key[0] == 'y' and not key in columns:
                    columns.append(key)

                # deve ser feito assim pois deve manter a ordem de entrada na lista
                # inviabilizando o uso do set
                if not key[0] == 'y':
                    row.append(value['total'])

            row.append(total)
            rows.append(row)

        columns.append('total')

        return [columns]+rows

    def catalog_issues(self,
                       json_data=None,
                       code=None,
                       doc_type=None,
                       limit=async_mongo_limit):
        """
        Recover general issues access log from the catalog.
        """

        if json_data:
            raw_data = json_data.read()
        else:
            query = u"code={0}".format(code)
            if doc_type:
                query = u"type={0}".format(doc_type)

            raw_data = urllib2.urlopen('{0}?{1}&limit={2}'.format(
                self._ratchet,
                query,
                limit)).read()

        data = json.loads(raw_data)

        rows = []
        columns = [u'journal', 'issue', 'accesses']

        for item in data:
            issn = item['code'][0:9]
            issue = item['code']
            total = item['total']
            del item['code']
            del item['type']
            del item['total']
            del item['issue']

            rows.append([issn, issue, total])

        return [columns]+rows

    def catalog_articles(self,
                         json_data=None,
                         code=None,
                         doc_type=None,
                         limit=async_mongo_limit):
        """
        Recover general articles access log from the catalog.
        """

        if json_data:
            raw_data = json_data.read()
        else:
            query = u"code={0}".format(code)
            if doc_type:
                query = u"type={0}".format(doc_type)

            raw_data = urllib2.urlopen('{0}?{1}&limit={2}'.format(
                self._ratchet,
                query,
                limit)).read()

        data = json.loads(raw_data)

        rows = []
        columns = [u'journal', 'issue', 'article', 'accesses']

        for item in data:
            article = item['code']
            issn = item['code'][0:9]
            issue = item['code'][0:17]
            total = item['total']
            del item['code']
            del item['type']
            del item['total']
            del item['issue']
            del item['journal']

            rows.append([issn, issue, article, total])

        return [columns]+rows

    def catalog_articles_year_as_x_axis(self,
                                        json_data=None,
                                        code=settings.RATCHET_CATALOG_CODE,
                                        doc_type=None,
                                        limit=async_mongo_limit):
        """
        Recover general articles access by month and year log from the catalog.
        Months as Label
        Year as X-axis
        accesses as Y-axis
        """

        req = '{0}?code={1}&limit{2}'.format(self._ratchet, code, limit)

        if json_data:
            raw_data = json_data.read()
        else:
            raw_data = urllib2.urlopen(req).read()

        data = json.loads(raw_data)[0]

        del data['total']
        del data['code']

        empty_months_range = {'%02d' % x: 0 for x in range(1, 13)}

        years = {}

        for key, value in data.items():
            #reading data from sci_arttext and download pages
            if key in ['sci_arttext', 'download']:
                del value['total']
                for year, months in value.items():
                    del months['total']
                    ye = years.setdefault(year[1:], copy.copy(empty_months_range))
                    for month, days in months.items():
                            ye[month[1:]] += days['total']

        rows = []
        rows.append([u'year'] + range(1, 13) + [u'total'])

        for year, months in OrderedDict(sorted(years.items())).items():
            row = []
            row.append(year)
            total = 0
            for month, value in OrderedDict(sorted(months.items())).items():
                total += int(value)
                row.append(value)
            row.append(total)
            rows.append(row)

        return rows

    def catalog_articles_month_as_x_axis(self,
                                         json_data=None,
                                         code=settings.RATCHET_CATALOG_CODE,
                                         doc_type=None,
                                         limit=async_mongo_limit):
        """
        Recover general articles access by month and year log from the catalog.
        Months as Label
        Year as X-axis
        accesses as Y-axis
        """

        req = '{0}?code={1}&limit{2}'.format(self._ratchet, code, limit)

        if json_data:
            raw_data = json_data.read()
        else:
            raw_data = urllib2.urlopen(req).read()

        data = json.loads(raw_data)[0]

        del data['total']
        del data['code']

        empty_months_range = {'%02d' % x: 0 for x in range(1, 13)}
        # Creating dict year that represents the sum of accesses of all available years
        # separated by months for the pages sci_arttext and download
        years = {}
        for key, value in data.items():
            #reading data from sci_arttext and download pages
            if key in ['sci_arttext', 'download']:
                del value['total']
                for year, months in value.items():
                    del months['total']
                    ye = years.setdefault(year[1:], copy.copy(empty_months_range))
                    for month, days in months.items():
                            ye[month[1:]] += days['total']

        rows = []
        for month in range(1, 13):
            row = []
            for year, months in OrderedDict(sorted(years.items())).items():
                if not len(row):
                    row.append(month)
                row.append(months['%02d' % month])
            rows.append(row)

        columns = [u'months']
        for year, months in OrderedDict(sorted(years.items())).items():
            columns.append(year)

        return [columns]+rows
