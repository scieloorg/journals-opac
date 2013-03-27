from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import cache_page

cache_minutes = 60 * 24
@cache_page(cache_minutes)
def journals(request):

    return render_to_response('accesses/journals.html', {
                              'page_index': 'catalog_journals',
                              },
                              context_instance=RequestContext(request))

@cache_page(cache_minutes)
def catalog_pages(request):

    return render_to_response('accesses/catalog_pages.html', {
                              'page_index': 'catalog_pages',
                              },
                              context_instance=RequestContext(request))

@cache_page(cache_minutes)
def catalog_journals(request):

    return render_to_response('accesses/catalog_journals.html', {
                              'page_index': 'catalog_journals',
                              },
                              context_instance=RequestContext(request))

@cache_page(cache_minutes)
def catalog_issues(request):

    return render_to_response('accesses/catalog_issues.html', {
                              'page_index': 'catalog_issues',
                              },
                              context_instance=RequestContext(request))

@cache_page(cache_minutes)
def catalog_articles(request):

    return render_to_response('accesses/catalog_articles.html', {
                              'page_index': 'catalog_articles',
                              },
                              context_instance=RequestContext(request))

@cache_page(cache_minutes)
def catalog_articles_month_year(request):

    return render_to_response('accesses/catalog_articles_month_year.html', {
                              'page_index': 'catalog_articles_month_year',
                              },
                              context_instance=RequestContext(request))
