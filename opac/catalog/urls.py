from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from catalog import views

urlpatterns = patterns('',

    # Collection Templates
    url(r'^$', direct_to_template, {'template': 'catalog/index.html'}),
    url(r'^alpha/$', views.list_journals, name="catalog.list_journals"),
    url(r'^subject/$', views.list_journals_by_subject, name="catalog.list_journals_by_subject"),
    url(r'^stats/$', direct_to_template, {'template': 'catalog/collection_stats.html'}),

    # Issue Templates
    url(r'^issues/(?P<journal_id>\w+)/', views.issues, name='catalog.show_issues'),
    url(r'^issue/(?P<journal_id>\w+)/(?P<issue_id>\d+)/', views.issue, name='catalog.show_issue'),

    # Journal Templates
    url(r'^journal/(?P<journal_id>\w+)/$', views.journal, name='catalog.journal'),
    url(r'^journal/(?P<journal_id>\w+)/stats/$', views.journal_stats, name='catalog.journal_stats'),

    # Ajax
    url(r'^ajx/ajx1/(?P<journal_id>\w+)/$', views.ajx_list_journal_tweets,
        name='catalog.ajx_list_journal_tweets'),
)
