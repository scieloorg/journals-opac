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
    url(r'^issue/(?P<journal_id>\d+)/(?P<issue_id>\d+)/', views.issue, name='catalog.show_issue'),

    # Journal Templates
    url(r'^journal/(?P<journal_id>\d+)/$', views.journal, name='catalog.journal'),
    url(r'^journal/(?P<journal_id>\d+)/stats/$', views.journal_stats, name='catalog.journal_stats'),
)
