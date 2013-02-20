import json

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext

from catalog import mongomodels
from catalog.tools import Navigation


def list_journals(request):

    journals_current = mongomodels.list_journals(criteria={'pub_status': 'current'})

    journals_non_current = mongomodels.list_journals(criteria={'pub_status': 'deceased'})

    return render_to_response('catalog/alpha.html', {
                              'journals_current': journals_current,
                              'journals_non_current': journals_non_current},
                               context_instance=RequestContext(request))


def list_journals_by_subject(request):

    journals = mongomodels.list_journals_by_study_areas()

    return render_to_response('catalog/subject.html', {
                              'journals': journals},
                              context_instance=RequestContext(request))


def journal(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id=journal_id)

    navigation = Navigation(journal)

    return render_to_response('catalog/journal.html', {
                              'journal': journal,
                              'navigation': navigation
                              },
                              context_instance=RequestContext(request))


def journal_stats(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id=journal_id)

    return render_to_response('catalog/journal_stats.html', {
                              'journal': journal},
                              context_instance=RequestContext(request))


def issues(request, journal_id):

    journal = mongomodels.Journal.get_journal(journal_id)
    issues = journal.list_issues_as_grid()

    return render_to_response('catalog/issues.html', {
                              'issues': issues},
                              context_instance=RequestContext(request))


def issue(request, journal_id, issue_id):

    issue = mongomodels.Issue.get_issue(journal_id, issue_id)
    journal = issue.journal
    sections = issue.list_sections()

    navigation = Navigation(journal, issue=issue)

    return render_to_response('catalog/issue.html', {
                              'sections': sections,
                              'issue': issue,
                              'navigation': navigation,
                              'journal': journal,
                              },
                              context_instance=RequestContext(request))


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
