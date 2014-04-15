# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Commutersurvey.other_greentravel'
        db.delete_column(u'survey_commutersurvey', 'other_greentravel')

        # Deleting field 'Commutersurvey.newsletter'
        db.delete_column(u'survey_commutersurvey', 'newsletter')

        # Deleting field 'Commutersurvey.to_work_today'
        db.delete_column(u'survey_commutersurvey', 'to_work_today')

        # Deleting field 'Commutersurvey.from_work_normally'
        db.delete_column(u'survey_commutersurvey', 'from_work_normally')

        # Deleting field 'Commutersurvey.to_work_normally'
        db.delete_column(u'survey_commutersurvey', 'to_work_normally')

        # Deleting field 'Commutersurvey.from_work_today'
        db.delete_column(u'survey_commutersurvey', 'from_work_today')

        # Deleting field 'Commutersurvey.work_location'
        db.delete_column(u'survey_commutersurvey', 'work_location')

        # Deleting field 'Commutersurvey.home_location'
        db.delete_column(u'survey_commutersurvey', 'home_location')


    def backwards(self, orm):
        # Adding field 'Commutersurvey.other_greentravel'
        db.add_column(u'survey_commutersurvey', 'other_greentravel',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Commutersurvey.newsletter'
        db.add_column(u'survey_commutersurvey', 'newsletter',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.to_work_today'
        db.add_column(u'survey_commutersurvey', 'to_work_today',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.from_work_normally'
        db.add_column(u'survey_commutersurvey', 'from_work_normally',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.to_work_normally'
        db.add_column(u'survey_commutersurvey', 'to_work_normally',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.from_work_today'
        db.add_column(u'survey_commutersurvey', 'from_work_today',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.work_location'
        db.add_column(u'survey_commutersurvey', 'work_location',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(default='POINT(0 0)', null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.home_location'
        db.add_column(u'survey_commutersurvey', 'home_location',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(default='POINT(0 0)', null=True, blank=True),
                      keep_default=False)


    models = {
        u'survey.commutersurvey': {
            'Meta': {'object_name': 'Commutersurvey'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'legs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Leg']", 'symmetrical': 'False'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '1', 'blank': 'True'}),
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
            'day': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['survey']