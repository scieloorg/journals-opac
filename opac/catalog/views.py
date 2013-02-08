import json

from django.shortcuts import render_to_response
from django.http import HttpResponse

from catalog import mongomodels


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


def issues(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id)
    issues = journal.list_issues_as_grid()

    return render_to_response('catalog/issues.html', {'issues': issues})


def issue(request, journal_id, issue_id):

    issue = mongomodels.Issue.get_issue(journal_id, issue_id)
    sections = issue.list_sections()

    return render_to_response('catalog/issue.html', {'sections': sections})


def ajx_list_journal_tweets(request, journal_id):
    """
    Lists the tweets of a given journal.
    """
    if not request.is_ajax():
        return HttpResponse(status=400)

    try:
        journal = mongomodels.Journal.get_journal(journal_id=journal_id)
    except ValueError:
        return HttpResponse(status=400)

    tweets = journal.tweets

    response_data = json.dumps(tweets)

    return HttpResponse(response_data, mimetype="application/json")
