# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Month'
        db.create_table(u'survey_month', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('url_month', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal(u'survey', ['Month'])


    def backwards(self, orm):
        # Deleting model 'Month'
        db.delete_table(u'survey_month')


    models = {
        u'survey.commutersurvey': {
            'Meta': {'object_name': 'Commutersurvey'},
            'affectedyou': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caltdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caltdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cpdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cpdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'gender_other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'health': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'lastweek': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'odays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'odaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outsidechanges': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tcdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tcdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'work_address': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'survey.employer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Employer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_parent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nr_employees': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.EmplSector']", 'null': 'True', 'blank': 'True'}),
            'size_cat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.EmplSizeCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.emplsector': {
            'Meta': {'object_name': 'EmplSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'survey.emplsizecategory': {
            'Meta': {'object_name': 'EmplSizeCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'survey.leg': {
            'Meta': {'object_name': 'Leg'},
            'commutersurvey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Commutersurvey']"}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'survey.month': {
            'Meta': {'object_name': 'Month'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'url_month': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['survey']