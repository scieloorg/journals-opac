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
    tab = ratchet.Accesses().catalog_journals(doc_type='journal')
    return {'tab': json.dumps(tab)}


@register.inclusion_tag('accesses/inctag_catalog_issues.html')
def catalog_issues(**attributes):
    tab = ratchet.Accesses().catalog_issues(doc_type='issue')
    return {'tab': json.dumps(tab)}


@register.inclusion_tag('accesses/inctag_catalog_articles.html')
def catalog_articles(**attributes):
    tab = ratchet.Accesses().catalog_articles(doc_type='article')
    return {'tab': json.dumps(tab)}


@register.inclusion_tag('accesses/inctag_catalog_articles_month_year.html')
def catalog_articles_month_year(**attributes):
    tab1 = ratchet.Accesses().catalog_articles_year_as_x_axis()
    tab2 = ratchet.Accesses().catalog_articles_month_as_x_axis()
    return {'tab1': json.dumps(tab1), 'tab2': json.dumps(tab2)}
