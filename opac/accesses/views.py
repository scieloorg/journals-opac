from django.shortcuts import render_to_response
from django.template.context import RequestContext

from accesses import ratchet


def journals(request):

    tab = ratchet.Accesses()

    return render_to_response('accesses/journals.html', {
                              'accesses': tab,
                              },
                              context_instance=RequestContext(request))


def catalog_pages(request):

    return render_to_response('accesses/catalog_pages.html', {
                              'catalog': 'pages',
                              },
                              context_instance=RequestContext(request))


def catalog_journals(request):

    return render_to_response('accesses/catalog_journals.html', {
                              'catalog': 'journals',
                              },
                              context_instance=RequestContext(request))


def catalog_issues(request):

    return render_to_response('accesses/catalog_issues.html', {
                              'catalog': 'issues',
                              },
                              context_instance=RequestContext(request))


def catalog_articles(request):

    return render_to_response('accesses/catalog_articles.html', {
                              'catalog': 'articles',
                              },
                              context_instance=RequestContext(request))


def catalog_articles_month_year(request):

    return render_to_response('accesses/catalog_articles_month_year.html', {
                              'catalog': 'articles_month_year',
                              },
                              context_instance=RequestContext(request))
