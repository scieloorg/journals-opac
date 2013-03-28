from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from catalog import views

urlpatterns = patterns('',

    # Collection Templates
    url(r'^alpha/$', views.list_journals, name="catalog.list_journals"),
    url(r'^subject/$', views.list_journals_by_subject, name="catalog.list_journals_by_subject"),

    # Issue Templates
    url(r'^issues/(?P<journal_id>\w+)/', views.issues, name='catalog.show_issues'),
    url(r'^issue/(?P<journal_id>\w+)/(?P<issue_id>\d+)/', views.issue, name='catalog.show_issue'),

    # Journal Templates
    url(r'^journal/(?P<journal_id>\w+)/$', views.journal, name='catalog.journal'),
    url(r'^journal/(?P<journal_id>\w+)/stats/$', views.journal_stats, name='catalog.journal_stats'),

    #Article Templates
    url(r'^article/(?P<article_id>[\w\-]+)/$', TemplateView.as_view(template_name='catalog/article.html'),
        name='catalog.article'),

    # Ajax
    url(r'^ajx/ajx1/(?P<journal_id>\w+)/$', views.ajx_list_journal_tweets,
        name='catalog.ajx_list_journal_tweets'),

    # i18n
    (r'^i18n/', include('django.conf.urls.i18n')),
)
