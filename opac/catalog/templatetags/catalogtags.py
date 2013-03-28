#encoding: utf-8

import json

from django import template
from django.http import Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from catalog.tools import try_get_content_by_lang

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
        snippet += u'<dt><i class="icon-chevron-right"></i> %s</dt>' % try_get_content_by_lang(section.titles, language)

        for article in section.articles:
            snippet += u'<dd><ul class="unstyled toc_article"><li>%s' % try_get_content_by_lang(article.title_group, language)
            snippet += u'<ul class="inline toc_article_authors">'

            for author in article.list_authors():
                snippet += u'<li><a href="#">%s, %s</a>;</li>' % (author['surname'], author['given_names'])
            snippet += u'</ul>'

            #Abstract list
            snippet += u'<ul class="inline toc_article_links"><li>%s: ' % _('abstract')
            snippet += u' | '.join(['<a href="%s?tlang=%s">%s</a>' % (reverse('catalog.article', args=[article.id]), key, key) for key in article.abstract.iterkeys()])
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


@register.simple_tag
def get_article_title_by_lang(title_group, language, default):

    return try_get_content_by_lang(title_group, language, default)


@register.simple_tag
def get_article_abstract_by_lang(abstract, language, default):

    return try_get_content_by_lang(abstract, language, default)


@register.simple_tag
def get_article_keywords_by_lang(keywords, language, default):

    return u'; '.join(keyword for keyword in try_get_content_by_lang(keywords, language, default))


@register.simple_tag
def list_authors(authors):

    snippet = u'; '.join(['%s, %s' % (author['surname'], author['given_names']) for author in authors])

    return snippet
