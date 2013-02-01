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


def journal_subject_list(areas_list):

    snippet = ''
    last_initial = None

    for areas in areas_list:
        snippet += u'<dl>'
        snippet += u'<dt>%s</dt>' % areas['area'].upper()
        snippet += u'<dd><dl><dd><ul class="unstyled">'
        for journal in areas['journals']:
            if last_initial and journal.title[0].lower() != last_initial.lower():
                snippet += u'<li>&nbsp;</li>'
            last_initial = journal.title[0]
            snippet += u'<li><a href="#">%s</a> - %s issues</li>' % (journal.title, journal.issues_count)

        snippet += '</ul></dd></dl></dd></dl>'

    return snippet

register.simple_tag(journal_subject_list)


def subject_list(areas_list):

    snippet = '<ul class="unstyled">'

    for area in areas_list:
        snippet += '<li><a href="#">%s</a></li>' % area['area']
    snippet += '</ul>'

    return snippet

register.simple_tag(subject_list)
