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


def journals_by_subject(journals):

    snippet = ''
    last_initial = None

    for area in journals:
        snippet += u'<dl>'
        snippet += u'<dt>%s</dt>' % area['area'].upper()
        snippet += u'<dd><dl><dd><ul class="unstyled">'
        for journal in area['journals']:
            if last_initial and journal.title[0].lower() != last_initial.lower():
                snippet += u'<li>&nbsp;</li>'
            last_initial = journal.title[0]
            snippet += u'<li><a href="#">%s</a> - %s issues</li>' % (journal.title, journal.issues_count)

        snippet += '</ul></dd></dl></dd></dl>'

    return snippet

register.simple_tag(journals_by_subject)


def subject_list(journals):

    snippet = '<ul class="unstyled">'

    for area in journals:
        snippet += '<li><a href="#">%s</a></li>' % area['area']
    snippet += '</ul>'

    return snippet

register.simple_tag(subject_list)
