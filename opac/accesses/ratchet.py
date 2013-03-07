import urllib2
import json

from django.conf import settings


class Accesses(object):

    def catalog_year(self):
        """
        Recover general access log from the catalog.
        """
        req = '{0}general?code=www.scielo.br'.format(settings.RATCHET_URI)

        data = json.loads(urllib2.urlopen(req).read())

        for key, value in data.items():
            if key[0] != 'y':
                del data[key]

        return data

    def catalog_pages(self, data=None):
        """
        Recover general access log from the catalog.
        """
        req = '{0}general?code=www.scielo.br'.format(settings.RATCHET_URI)

        if not data:
            data = json.loads(urllib2.urlopen(req).read())

        del data['code']

        tab = {}
        tab['columns'] = []
        tab['rows'] = {}
        for key, value in data.items():
            if key[0] == 'y':
                del data[key]
            else:
                tab['columns'].append(key)
                for year, months in value.items():
                    del months['total']
                    for month, days in months.items():
                        dat = year[1:] + month[1:]
                        l = tab['rows'].setdefault(dat, [])
                        l.append(days['total'])

        rows = []
        columns = [u'year']
        for column in tab['columns']:
            columns.append(column)
        rows.append(columns)
        for key, values in tab['rows'].items():
            row = []
            row.append(key)
            for value in values:
                row.append(value)

            rows.append(row)

        return rows
