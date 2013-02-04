from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from catalog import views

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'catalog/index.html'}),
    url(r'^alpha/$', views.list_journals, name="catalog.list_journals"),
    url(r'^subject/$', views.list_journals_by_subject, name="catalog.list_journals_by_subject"),
    url(r'^usage/$', direct_to_template, {'template': 'catalog/usage.html'}),
    url(r'^journal/$', direct_to_template, {'template': 'catalog/journal.html'}),
    url(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/', views.issue, name='issue.html'),
)
