from django import template
from django.utils.translation import ugettext as _

register = template.Library()


def journal_alpha_list(journals):

    snippet = u'<ul class="unstyled">'
    last_initial = None

    for journal in journals:
        if last_initial and journal.title[0].lower() != last_initial.lower():
            snippet += u'<li>&nbsp;</li>'
        last_initial = journal.title[0]
        snippet += u'<li><a href="#">%s</a> - %s %s</li>' % (journal.title, unicode(journal.issues_count), _('issues'))

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
            snippet += u'<li><a href="#">%s</a> - %s %s</li>' % (journal.title, journal.issues_count, _('issues'))

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


def issues_list_with_articles(sections, language):

    snippet = u'<dl class="issue_toc">'

    for section in sections:
        snippet += u'<dt><i class="icon-chevron-right"></i> %s</dt>' % section.titles[language]
        for article in section.articles:
            snippet += u'<dd><ul class="unstyled toc_article"><li>%s' % article.title_group[language]
            snippet += u'<ul class="inline toc_article_authors">'
            for author in article.list_authors():
                snippet += u'<li><a href="#">%s, %s</a>;</li>' % (author['surname'], author['given_names'])
            snippet += u'</ul>'
            snippet += u'<ul class="inline toc_article_links"><li>%s: ' % _('abstract')
            snippet += u' | '.join(['<a href="#">%s</a> ' % key for key in article.abstract.iterkeys()])
    snippet += u'</li></ul></li></dl>'

    return snippet

register.simple_tag(issues_list_with_articles)
