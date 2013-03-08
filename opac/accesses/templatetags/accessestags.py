import json

from django import template

from accesses import ratchet

register = template.Library()


@register.inclusion_tag('accesses/inctag_catalog.html')
def catalog_chart(**attributes):

    tab = ratchet.Accesses().catalog_pages()
    return {'tab': json.dumps(tab)}
