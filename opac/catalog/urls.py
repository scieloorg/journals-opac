from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'catalog/index.html'}),
    url(r'^alpha/$', direct_to_template, {'template': 'catalog/alpha.html'}),

)
