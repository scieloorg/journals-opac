import json

from catalog import mongomodels
from django.shortcuts import render_to_response
from django.http import HttpResponse


def list_journals(request):

    journals = mongomodels.list_journals()

    return render_to_response('catalog/alpha.html', {'journals': journals})


def list_journals_by_subject(request):

    journals = mongomodels.list_journals_by_study_areas()

    return render_to_response('catalog/subject.html', {'journals': journals})


def journal(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id=journal_id)

    return render_to_response('catalog/journal.html', {'journal': journal})


def journal_stats(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id=journal_id)

    return render_to_response('catalog/journal_stats.html', {'journal': journal})


def ajx_list_journal_tweets(request, journal_id):
    """
    Lists the tweets of a given journal.
    """
    if not request.is_ajax():
        return HttpResponse(status=400)

    journal = mongomodels.Journal.get_journal(journal_id=journal_id)

    tweets = journal.tweets

    response_data = json.dumps(tweets)

    return HttpResponse(response_data, mimetype="application/json")
