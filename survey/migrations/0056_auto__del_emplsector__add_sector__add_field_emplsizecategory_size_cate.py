# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'EmplSector'
        db.delete_table(u'survey_emplsector')

        # Adding model 'Sector'
        db.create_table(u'survey_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Sector'])

        # Adding field 'EmplSizeCategory.size_category'
        db.add_column(u'survey_emplsizecategory', 'size_category',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Employer.is_parent'
        db.delete_column(u'survey_employer', 'is_parent')


        # Changing field 'Employer.sector'
        db.alter_column(u'survey_employer', 'sector_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Sector'], null=True))
        # Deleting field 'Commutersurvey.employer_legacy'
        db.delete_column(u'survey_commutersurvey', 'employer_legacy')


    def backwards(self, orm):
        # Adding model 'EmplSector'
        db.create_table(u'survey_emplsector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'survey', ['EmplSector'])

        # Deleting model 'Sector'
        db.delete_table(u'survey_sector')

        # Deleting field 'EmplSizeCategory.size_category'
        db.delete_column(u'survey_emplsizecategory', 'size_category')

        # Adding field 'Employer.is_parent'
        db.add_column(u'survey_employer', 'is_parent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Employer.sector'
        db.alter_column(u'survey_employer', 'sector_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.EmplSector'], null=True))
        # Adding field 'Commutersurvey.employer_legacy'
        db.add_column(u'survey_commutersurvey', 'employer_legacy',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    models = {
        u'survey.commutersurvey': {
            'Meta': {'object_name': 'Commutersurvey'},
            'already_green': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calorie_change': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'carbon_change': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'change_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Employer']", 'null': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'share': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Team']", 'null': 'True', 'blank': 'True'}),
            'volunteer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wr_day_month': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Month']"})
        },
        u'survey.employer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Employer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nr_employees': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Sector']", 'null': 'True', 'blank': 'True'}),
            'size_cat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.EmplSizeCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.emplsizecategory': {
            'Meta': {'object_name': 'EmplSizeCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'size_category': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
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
        u'survey.sector': {
            'Meta': {'object_name': 'Sector'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'survey.team': {
            'Meta': {'object_name': 'Team'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Employer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['survey']