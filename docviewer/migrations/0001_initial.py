# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Document'
        db.create_table('docviewer_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('status', self.gf('model_utils.fields.StatusField')(default='waiting', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor='status')),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique=True, max_length=255, populate_from=None, unique_with=(), db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True, blank=True)),
            ('page_count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('contributor_organization', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('docviewer', ['Document'])

        # Adding model 'Page'
        db.create_table('docviewer_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pages_set', to=orm['docviewer.Document'])),
            ('page', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('docviewer', ['Page'])

        # Adding model 'Section'
        db.create_table('docviewer_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections_set', to=orm['docviewer.Document'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('page', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('docviewer', ['Section'])

        # Adding model 'Annotation'
        db.create_table('docviewer_annotation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document', self.gf('django.db.models.fields.related.ForeignKey')(related_name='annotations_set', to=orm['docviewer.Document'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
            ('page', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('docviewer', ['Annotation'])


    def backwards(self, orm):
        
        # Deleting model 'Document'
        db.delete_table('docviewer_document')

        # Deleting model 'Page'
        db.delete_table('docviewer_page')

        # Deleting model 'Section'
        db.delete_table('docviewer_section')

        # Deleting model 'Annotation'
        db.delete_table('docviewer_annotation')


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
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'page_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'waiting'", 'max_length': '100', 'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', 'monitor': "'status'"}),
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
