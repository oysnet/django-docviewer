# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.language'
        db.add_column(u'docviewer_document', 'language',
                      self.gf('django.db.models.fields.CharField')(default='spa', max_length=7),
                      keep_default=False)

        # Adding field 'Document.docfile'
        db.add_column(u'docviewer_document', 'docfile',
                      self.gf('django.db.models.fields.files.FileField')(max_length=512, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Document.slug'
        db.alter_column(u'docviewer_document', 'slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=255, populate_from='title', unique_with=()))

        # Changing field 'Document.related_url'
        db.alter_column(u'docviewer_document', 'related_url', self.gf('django.db.models.fields.URLField')(max_length=1024))

    def backwards(self, orm):
        # Deleting field 'Document.language'
        db.delete_column(u'docviewer_document', 'language')

        # Deleting field 'Document.docfile'
        db.delete_column(u'docviewer_document', 'docfile')


        # Changing field 'Document.slug'
        db.alter_column(u'docviewer_document', 'slug', self.gf('autoslug.fields.AutoSlugField')(max_length=255, unique_with=(), unique=True, populate_from=None))

        # Changing field 'Document.related_url'
        db.alter_column(u'docviewer_document', 'related_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True))

    models = {
        u'docviewer.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'annotations_set'", 'to': u"orm['docviewer.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'docviewer.document': {
            'Meta': {'object_name': 'Document'},
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contributor_organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'download': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'spa'", 'max_length': '7'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'related_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "'title'", 'unique_with': '()'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'waiting'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
            'task_error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'task_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'docviewer.page': {
            'Meta': {'object_name': 'Page'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages_set'", 'to': u"orm['docviewer.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'docviewer.section': {
            'Meta': {'object_name': 'Section'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections_set'", 'to': u"orm['docviewer.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['docviewer']