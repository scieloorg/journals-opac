from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'catalog/index.html'}),
    url(r'^alpha/$', direct_to_template, {'template': 'catalog/alpha.html'}),
    url(r'^subject/$', direct_to_template, {'template': 'catalog/subject.html'}),
    url(r'^usage/$', direct_to_template, {'template': 'catalog/usage.html'}),
    url(r'^journal/$', direct_to_template, {'template': 'catalog/journal.html'}),
    url(r'^issue/$', direct_to_template, {'template': 'catalog/issue.html'}),

)
