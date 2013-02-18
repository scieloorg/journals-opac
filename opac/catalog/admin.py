# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import patterns
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from . import models
from utils import tasks


class CollectionMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_member')
    list_filter = ('is_member', )
    ordering = ('name', )
    readonly_fields = ('name', 'name_slug', 'resource_uri',)

    def get_urls(self):
        urls = super(CollectionMetaAdmin, self).get_urls()
        new_urls = patterns('',
            (r'^sync_collectionsmeta/$', self.sync_collectionsmeta)
        )

        return new_urls + urls

    def sync_collectionsmeta(self, request):
        tasks.sync_collections_meta()

        return HttpResponseRedirect(
            urlresolvers.reverse('admin:catalog_collectionmeta_changelist')
        )


admin.site.register(models.CollectionMeta, CollectionMetaAdmin)
admin.site.register(models.JournalMeta)
