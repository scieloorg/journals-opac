from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from accesses import views

urlpatterns = patterns('',

    # Accesses Templates
    url(r'^$', TemplateView.as_view(template_name='accesses/catalog_stats.html')),
    url(r'^journals/$', views.journals, name="accesses.journals"),
    url(r'^catalog/pages/$', views.catalog_pages, name="accesses.catalog_pages"),
    url(r'^catalog/journals/$', views.catalog_journals, name="accesses.catalog_journals"),
)
