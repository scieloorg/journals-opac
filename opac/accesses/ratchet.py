import urllib2
import json
from collections import OrderedDict

from django.conf import settings


class Accesses(object):

    def __init__(self, ratchet_uri=settings.RATCHET_URI, resource='general'):
        self._ratchet = '{0}{1}?code='.format(ratchet_uri, resource)

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

    def catalog_pages(self,
                      json_data=None,
                      code=settings.RATCHET_CATALOG_CODE):
        """
        Recover general access log from the catalog.
        """
        req = '{0}{1}'.format(self._ratchet, code)

        try:
            if json_data:
                data = json.loads(json_data.read())
            else:
                data = json.loads(urllib2.urlopen(req).read())
        except ValueError:
            return []

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
                        dat = u'{0}-{1}'.format(year[1:], month[1:])
                        l = tab['rows'].setdefault(dat, [])
                        l.append(days['total'])

        rows = []
        rows.append([u'year'] + tab['columns'])
        for key, values in OrderedDict(sorted(tab['rows'].items())).items():
            row = []
            row.append(key)
            for value in values:
                row.append(value)

            rows.append(row)

        return rows
