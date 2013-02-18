# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages
from django.conf.urls import patterns
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from . import models
from utils.tasks import full_sync
from utils.tasks import sync_collections_meta


class CollectionMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_member')
    list_filter = ('is_member', )
    ordering = ('name', )
    readonly_fields = ('name', 'name_slug', 'resource_uri',)

    def get_urls(self):
        urls = super(CollectionMetaAdmin, self).get_urls()
        new_urls = patterns('',
            (r'^sync_collectionsmeta/$', self.sync_collectionsmeta),
            (r'^sync_catalog/$', self.sync_catalog),
        )

        return new_urls + urls

    def sync_collectionsmeta(self, request):
        sync_collections_meta()

        messages.info(request, 'The list of collections is now up-to-date.')
        return HttpResponseRedirect(
            urlresolvers.reverse('admin:catalog_collectionmeta_changelist')
        )

    def sync_catalog(self, request):
        full_sync.delay()

        messages.info(request, 'The catalog is being built. It may take some time, please be patient.')

        return HttpResponseRedirect(
            urlresolvers.reverse('admin:catalog_collectionmeta_changelist')
        )


admin.site.register(models.CollectionMeta, CollectionMetaAdmin)
admin.site.register(models.JournalMeta)
