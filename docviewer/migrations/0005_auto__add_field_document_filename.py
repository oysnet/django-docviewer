# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Document.filename'
        db.add_column('docviewer_document', 'filename', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Document.filename'
        db.delete_column('docviewer_document', 'filename')


    models = {
        'docviewer.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'annotations_set'", 'to': "orm['docviewer.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'docviewer.document': {
            'Meta': {'object_name': 'Document'},
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contributor_organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime(2012, 3, 8, 9, 17, 46, 626516)'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'download': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime(2012, 3, 8, 9, 17, 46, 626649)'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'related_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'waiting'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime(2012, 3, 8, 9, 17, 46, 626882)', 'monitor': "'status'"}),
            'task_error': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'task_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'docviewer.page': {
            'Meta': {'object_name': 'Page'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages_set'", 'to': "orm['docviewer.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'docviewer.section': {
            'Meta': {'object_name': 'Section'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections_set'", 'to': "orm['docviewer.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['docviewer']
