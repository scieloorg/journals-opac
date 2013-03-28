# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages
from django.conf.urls import patterns
from django.core import urlresolvers
from django.http import HttpResponseRedirect

from . import models
from utils.tasks import build_catalog
from utils.tasks import sync_collections_meta
from utils.tasks import sync_journals_meta


class CollectionMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_member')
    list_filter = ('is_member', )
    ordering = ('name', )
    readonly_fields = ('name', 'name_slug', 'resource_uri',)
    actions = ['make_collections_as_members', 'make_collections_not_as_members']

    def make_collections_as_members(self, request, queryset):
        queryset.update(is_member=True)
    make_collections_as_members.short_description = 'Mark selected as members of the catalog'

    def make_collections_not_as_members(self, request, queryset):
        queryset.update(is_member=False)
    make_collections_not_as_members.short_description = 'Mark selected NOT as members of the catalog'

    def get_actions(self, request):
        actions = super(CollectionMetaAdmin, self).get_actions(request)
        actions.pop('delete_selected', None)

        return actions

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
        build_catalog.delay()

        messages.info(request, 'The catalog is being built. It may take some time, please be patient.')

        return HttpResponseRedirect(
            urlresolvers.reverse('admin:catalog_collectionmeta_changelist')
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class JournalMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'is_member')
    list_filter = ('is_member', 'collection__name', )
    ordering = ('name', )
    readonly_fields = ('name', 'resource_uri', 'collection')
    actions = ['make_collections_as_members', 'make_collections_not_as_members']

    def make_collections_as_members(self, request, queryset):
        queryset.update(is_member=True)
    make_collections_as_members.short_description = 'Mark selected as members of the catalog'

    def make_collections_not_as_members(self, request, queryset):
        queryset.update(is_member=False)
    make_collections_not_as_members.short_description = 'Mark selected NOT as members of the catalog'

    def get_actions(self, request):
        actions = super(JournalMetaAdmin, self).get_actions(request)
        actions.pop('delete_selected', None)

        return actions

    def get_urls(self):
        urls = super(JournalMetaAdmin, self).get_urls()
        new_urls = patterns('',
            (r'^sync_journalsmeta/$', self.sync_journalsmeta),
            (r'^sync_catalog/$', self.sync_catalog),
        )

        return new_urls + urls

    def sync_journalsmeta(self, request):
        sync_journals_meta()

        messages.info(request, 'The list of journals is now up-to-date.')
        return HttpResponseRedirect(
            urlresolvers.reverse('admin:catalog_journalmeta_changelist')
        )

    def sync_catalog(self, request):
        build_catalog.delay()

        messages.info(request, 'The catalog is being built. It may take some time, please be patient.')

        return HttpResponseRedirect(
            urlresolvers.reverse('admin:catalog_journalmeta_changelist')
        )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SyncAdmin(admin.ModelAdmin):
    list_display = ('started_at', 'ended_at', 'last_seq', 'status')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.CollectionMeta, CollectionMetaAdmin)
admin.site.register(models.JournalMeta, JournalMetaAdmin)
admin.site.register(models.Sync, SyncAdmin)
