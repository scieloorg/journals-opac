from django import template

register = template.Library()


def journal_alpha_list(journals):

    snippet = u'<ul class="unstyled">'
    last_initial = None
    for journal in journals:
        if last_initial and journal.title[0].lower() != last_initial.lower():
            snippet += u'<li>&nbsp;</li>'
        last_initial = journal.title[0]
        snippet += u'<li><a href="#">%s</a> - %s issues</li>' % (journal.title, unicode(journal.issues_count))

    snippet += u'</ul>'

    return snippet

register.simple_tag(journal_alpha_list)
