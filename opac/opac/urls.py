from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',

    url(r'', include('catalog.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('flatpages_i18n.views', (r'^(?P<url>.*)$', 'flatpage'),)

if settings.DEBUG:

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )
