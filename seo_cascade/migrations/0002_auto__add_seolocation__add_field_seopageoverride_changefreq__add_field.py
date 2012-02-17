# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SEOLocation'
        db.create_table('seo_cascade_seolocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('omit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('changefreq', self.gf('django.db.models.fields.CharField')(default='weekly', max_length=50, null=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('priority', self.gf('django.db.models.fields.DecimalField')(default=0.5, null=True, max_digits=2, decimal_places=1, blank=True)),
        ))
        db.send_create_signal('seo_cascade', ['SEOLocation'])

        # Adding field 'SEOPageOverride.changefreq'
        db.add_column('seo_cascade_seopageoverride', 'changefreq', self.gf('django.db.models.fields.CharField')(default='weekly', max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'SEOModelDefault.changefreq'
        db.add_column('seo_cascade_seomodeldefault', 'changefreq', self.gf('django.db.models.fields.CharField')(default='weekly', max_length=50, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'SEOLocation'
        db.delete_table('seo_cascade_seolocation')

        # Deleting field 'SEOPageOverride.changefreq'
        db.delete_column('seo_cascade_seopageoverride', 'changefreq')

        # Deleting field 'SEOModelDefault.changefreq'
        db.delete_column('seo_cascade_seomodeldefault', 'changefreq')


    models = {
        'seo_cascade.seolocation': {
            'Meta': {'ordering': "['path']", 'object_name': 'SEOLocation'},
            'changefreq': ('django.db.models.fields.CharField', [], {'default': "'weekly'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'omit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'priority': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'null': 'True', 'max_digits': '2', 'decimal_places': '1', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'seo_cascade.seomodeldefault': {
            'Meta': {'ordering': "['model']", 'object_name': 'SEOModelDefault'},
            'changefreq': ('django.db.models.fields.CharField', [], {'default': "'weekly'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
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
            'changefreq': ('django.db.models.fields.CharField', [], {'default': "'weekly'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
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
