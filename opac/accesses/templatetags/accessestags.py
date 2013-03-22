import json

from django import template

from accesses import ratchet

register = template.Library()


@register.inclusion_tag('accesses/inctag_catalog_pages.html')
def catalog_pages(**attributes):
    tab = ratchet.Accesses().catalog_pages()
    return {'tab': json.dumps(tab)}


@register.inclusion_tag('accesses/inctag_catalog_journals.html')
def catalog_journals(**attributes):
    tab = ratchet.Accesses().catalog_journals()
    return {'tab': json.dumps(tab)}
