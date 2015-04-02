# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Commutersurvey.month'
        db.delete_column(u'survey_commutersurvey', 'month')


    def backwards(self, orm):
        # Adding field 'Commutersurvey.month'
        db.add_column(u'survey_commutersurvey', 'month',
                      self.gf('django.db.models.fields.CharField')(default='Placeholder Date', max_length=50),
                      keep_default=False)


    models = {
        u'survey.commutersurvey': {
            'Meta': {'object_name': 'Commutersurvey'},
            'affectedyou': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'already_green': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'bdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'calorie_change': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'caltdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caltdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'carbon_change': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'cdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'change_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cpdays': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cpdaysaway': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Employer']", 'null': 'True'}),
            'employer_legacy': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'gender_other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'health': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'lastweek': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'work_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wr_day_month': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Month']"})
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
            'calories': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'carbon': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'commutersurvey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Commutersurvey']"}),
            'day': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'new_mode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Mode']"})
        },
        u'survey.mode': {
            'Meta': {'object_name': 'Mode'},
            'carb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'green': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'met': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'survey.month': {
            'Meta': {'ordering': "['wr_day']", 'object_name': 'Month'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'close_checkin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_checkin': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'wr_day': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'survey.team': {
            'Meta': {'object_name': 'Team'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Employer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['survey']