# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SEOModelDefault'
        db.create_table('seo_cascade_seomodeldefault', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('omit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('model', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('priority', self.gf('django.db.models.fields.DecimalField')(default=0.5, null=True, max_digits=2, decimal_places=1, blank=True)),
        ))
        db.send_create_signal('seo_cascade', ['SEOModelDefault'])

        # Adding model 'SEOPageOverride'
        db.create_table('seo_cascade_seopageoverride', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('omit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('seo_cascade', ['SEOPageOverride'])


    def backwards(self, orm):
        
        # Deleting model 'SEOModelDefault'
        db.delete_table('seo_cascade_seomodeldefault')

        # Deleting model 'SEOPageOverride'
        db.delete_table('seo_cascade_seopageoverride')


    models = {
        'seo_cascade.seomodeldefault': {
            'Meta': {'ordering': "['model']", 'object_name': 'SEOModelDefault'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'omit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'null': 'True', 'max_digits': '2', 'decimal_places': '1', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'seo_cascade.seopageoverride': {
            'Meta': {'ordering': "['path']", 'object_name': 'SEOPageOverride'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'omit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['seo_cascade']
