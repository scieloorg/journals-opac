from catalog import mongomodels
from django.shortcuts import render_to_response


def list_journals(request):
    journals = mongomodels.list_journals()

    return render_to_response('catalog/alpha.html', {'journals': journals})


def list_journals_by_subject(request):
    pass
