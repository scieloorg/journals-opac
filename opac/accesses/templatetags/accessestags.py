import json

from django import template

from django.conf import settings

from accesses import ratchet

register = template.Library()


@register.simple_tag
def catalog_chart(**attributes):

    tab = ratchet.Accesses().catalog_pages()

    rows = []
    columns = ['year']
    for column in tab['columns']:
        columns.append(column)
    rows.append(columns)
    for key, values in tab['rows'].items():
        row = []
        row.append(key)
        for value in values:
            row.append(value)

        rows.append(row)

    js = """<script type="text/javascript">
        google.load('visualization', '1', {packages: ['table', 'corechart']});
        google.setOnLoadCallback(drawCharts);

        function drawCharts() {
          var data = new google.visualization.arrayToDataTable(%s);

          var table = new google.visualization.Table(document.getElementById('table_div'));
          table.draw(data);

          options = {
                'title': 'Catalog Accesses by page type',
                'vAxis': {'title': 'acceses'},
                'hAxis': {'title': 'months' }
          }

          var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
          chart.draw(data, options);

        }
        </script>""" % (json.dumps(rows))

    return js