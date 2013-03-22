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
