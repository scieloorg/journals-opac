from django import template
from django.utils.translation import ugettext as _

register = template.Library()


def list_articles_by_section(sections, language):

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
            snippet += u'</li></ul></li></dd>'

    snippet += u'</dl>'

    return snippet

register.simple_tag(list_articles_by_section)
