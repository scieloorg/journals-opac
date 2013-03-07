from django.shortcuts import render_to_response
from django.template.context import RequestContext

from accesses import ratchet


def journals(request):

    tab = ratchet.Accesses()

    return render_to_response('accesses/journals.html', {
                              'accesses': tab,
                              },
                              context_instance=RequestContext(request))


def catalog(request):

    tab = ratchet.Accesses().catalog_pages()

    return render_to_response('accesses/catalog.html', {
                              'pages': tab,
                              },
                              context_instance=RequestContext(request))
