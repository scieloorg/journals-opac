from catalog import mongomodels
from django.shortcuts import render_to_response


def list_journals(request):

    journals = mongomodels.list_journals()

    return render_to_response('catalog/alpha.html', {'journals': journals})


def list_journals_by_subject(request):
    pass


def journal(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id=journal_id)

    return render_to_response('catalog/journal.html', {'journal': journal})
