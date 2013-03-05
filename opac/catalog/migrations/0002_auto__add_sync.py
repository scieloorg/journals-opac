# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sync'
        db.create_table(u'catalog_sync', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_seq', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='started', max_length=32)),
        ))
        db.send_create_signal(u'catalog', ['Sync'])


    def backwards(self, orm):
        # Deleting model 'Sync'
        db.delete_table(u'catalog_sync')


    models = {
        u'catalog.collectionmeta': {
            'Meta': {'object_name': 'CollectionMeta'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'catalog.journalmeta': {
            'Meta': {'object_name': 'JournalMeta'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journals'", 'to': u"orm['catalog.CollectionMeta']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'catalog.sync': {
            'Meta': {'ordering': "['-ended_at']", 'object_name': 'Sync'},
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seq': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'started'", 'max_length': '32'})
        }
    }

    complete_apps = ['catalog']