import json

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django.conf import settings

register = template.Library()


@register.simple_tag
def ratchet_caller(**attributes):

    if settings.DEBUG:
        return ''

    attributes['ratchet_uri'] = settings.RATCHET_URI
    js = json.dumps(attributes)
    snippet = u'ratchet_obj = {0}; send_access(ratchet_obj);'.format(js)

    return snippet


@register.simple_tag
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

            #Abstract list
            snippet += u'<ul class="inline toc_article_links"><li>%s: ' % _('abstract')
            snippet += u' | '.join(['<a href="#">%s</a>' % key for key in article.abstract.iterkeys()])
            snippet += '</li>'

            #Full text list
            snippet += u'<li>%s: ' % _('full text')
            snippet += u'<a href="%s">%s</a></li>' % (reverse('catalog.article', args=[article.id]), article.default_language)

            #PDF list
            snippet += '<li>%s: ' % 'pdf'
            snippet += u'<a href="#">%s</a></li>' % article.default_language

            snippet += '</ul></li></dd>'
    snippet += u'</dl>'

    return snippet
