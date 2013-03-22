import urllib2
import json
from collections import OrderedDict

from django.conf import settings


class Accesses(object):

    def __init__(self, ratchet_uri=settings.RATCHET_URI, resource='general'):
        self._ratchet = '{0}{1}'.format(ratchet_uri, resource)

    def catalog_pages(self,
                      json_data=None,
                      code=settings.RATCHET_CATALOG_CODE):
        """
        Recover general access log from the catalog.
        """
        req = '{0}?code={1}'.format(self._ratchet, code)

        try:
            if json_data:
                data = json.loads(json_data.read())[0]
            else:
                data = json.loads(urllib2.urlopen(req).read())[0]
        except ValueError:
            return []

        del data['code']
        del data['total']

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
        rows.append([u'date'] + tab['columns'])
        for key, values in OrderedDict(sorted(tab['rows'].items())).items():
            row = []
            row.append(key)
            for value in values:
                row.append(value)

            rows.append(row)

        return rows

    def catalog_journals(self,
                         json_data=None,
                         code=None,
                         doc_type=None):
        """
        Recover general journals access log from the catalog.
        """

        try:
            if json_data:
                data = json.loads(json_data.read())
            else:
                query = u"code={0}".format(code)
                if doc_type:
                    query = u"type={0}".format(doc_type)
                data = json.loads(urllib2.urlopen(self._ratchet, query).read())
        except ValueError:
            return []

        rows = []
        columns = [u'journal']

        for item in data:
            row = []
            issn = item['code']
            total = item['total']
            del item['code']
            del item['type']
            del item['total']

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
