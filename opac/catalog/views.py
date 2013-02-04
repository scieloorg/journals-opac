from catalog import mongomodels
from django.shortcuts import render_to_response


def list_journals(request):
    journals = mongomodels.list_journals()

    return render_to_response('catalog/alpha.html', {'journals': journals})


def list_journals_by_subject(request):
    journals = mongomodels.list_journals_by_study_areas()

    return render_to_response('catalog/subject.html', {'journals': journals})


def issue(request, journal_id, issue_id):
    issue = mongomodels.Issue.get_issue(journal_id, issue_id)
    sections = issue.list_sections()
    return render_to_response('catalog/issue.html', {'sections': sections})
