# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CollectionMeta'
        db.create_table('catalog_collectionmeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resource_uri', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name_slug', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('catalog', ['CollectionMeta'])

        # Adding model 'JournalMeta'
        db.create_table('catalog_journalmeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_member', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resource_uri', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='journals', to=orm['catalog.CollectionMeta'])),
        ))
        db.send_create_signal('catalog', ['JournalMeta'])


    def backwards(self, orm):
        # Deleting model 'CollectionMeta'
        db.delete_table('catalog_collectionmeta')

        # Deleting model 'JournalMeta'
        db.delete_table('catalog_journalmeta')


    models = {
        'catalog.collectionmeta': {
            'Meta': {'object_name': 'CollectionMeta'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'catalog.journalmeta': {
            'Meta': {'object_name': 'JournalMeta'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journals'", 'to': "orm['catalog.CollectionMeta']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_member': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['catalog']