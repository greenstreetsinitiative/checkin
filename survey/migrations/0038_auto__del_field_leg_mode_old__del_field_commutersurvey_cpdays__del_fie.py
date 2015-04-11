# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Leg.mode_old'
        db.delete_column(u'survey_leg', 'mode_old')

        # Deleting field 'Commutersurvey.cpdays'
        db.delete_column(u'survey_commutersurvey', 'cpdays')

        # Deleting field 'Commutersurvey.caltdays'
        db.delete_column(u'survey_commutersurvey', 'caltdays')

        # Deleting field 'Commutersurvey.bdays'
        db.delete_column(u'survey_commutersurvey', 'bdays')

        # Deleting field 'Commutersurvey.odays'
        db.delete_column(u'survey_commutersurvey', 'odays')

        # Deleting field 'Commutersurvey.outsidechanges'
        db.delete_column(u'survey_commutersurvey', 'outsidechanges')

        # Deleting field 'Commutersurvey.cpdaysaway'
        db.delete_column(u'survey_commutersurvey', 'cpdaysaway')

        # Deleting field 'Commutersurvey.from_work_switch'
        db.delete_column(u'survey_commutersurvey', 'from_work_switch')

        # Deleting field 'Commutersurvey.lastweek'
        db.delete_column(u'survey_commutersurvey', 'lastweek')

        # Deleting field 'Commutersurvey.rdaysaway'
        db.delete_column(u'survey_commutersurvey', 'rdaysaway')

        # Deleting field 'Commutersurvey.cdaysaway'
        db.delete_column(u'survey_commutersurvey', 'cdaysaway')

        # Deleting field 'Commutersurvey.health'
        db.delete_column(u'survey_commutersurvey', 'health')

        # Deleting field 'Commutersurvey.odaysaway'
        db.delete_column(u'survey_commutersurvey', 'odaysaway')

        # Deleting field 'Commutersurvey.caltdaysaway'
        db.delete_column(u'survey_commutersurvey', 'caltdaysaway')

        # Deleting field 'Commutersurvey.tdays'
        db.delete_column(u'survey_commutersurvey', 'tdays')

        # Deleting field 'Commutersurvey.height'
        db.delete_column(u'survey_commutersurvey', 'height')

        # Deleting field 'Commutersurvey.bdaysaway'
        db.delete_column(u'survey_commutersurvey', 'bdaysaway')

        # Deleting field 'Commutersurvey.gender'
        db.delete_column(u'survey_commutersurvey', 'gender')

        # Deleting field 'Commutersurvey.tcdaysaway'
        db.delete_column(u'survey_commutersurvey', 'tcdaysaway')

        # Deleting field 'Commutersurvey.gender_other'
        db.delete_column(u'survey_commutersurvey', 'gender_other')

        # Deleting field 'Commutersurvey.affectedyou'
        db.delete_column(u'survey_commutersurvey', 'affectedyou')

        # Deleting field 'Commutersurvey.weight'
        db.delete_column(u'survey_commutersurvey', 'weight')

        # Deleting field 'Commutersurvey.wdays'
        db.delete_column(u'survey_commutersurvey', 'wdays')

        # Deleting field 'Commutersurvey.wdaysaway'
        db.delete_column(u'survey_commutersurvey', 'wdaysaway')

        # Deleting field 'Commutersurvey.tdaysaway'
        db.delete_column(u'survey_commutersurvey', 'tdaysaway')

        # Deleting field 'Commutersurvey.to_work_switch'
        db.delete_column(u'survey_commutersurvey', 'to_work_switch')

        # Deleting field 'Commutersurvey.tcdays'
        db.delete_column(u'survey_commutersurvey', 'tcdays')

        # Deleting field 'Commutersurvey.rdays'
        db.delete_column(u'survey_commutersurvey', 'rdays')

        # Deleting field 'Commutersurvey.cdays'
        db.delete_column(u'survey_commutersurvey', 'cdays')


    def backwards(self, orm):
        # Adding field 'Leg.mode_old'
        db.add_column(u'survey_leg', 'mode_old',
                      self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cpdays'
        db.add_column(u'survey_commutersurvey', 'cpdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.caltdays'
        db.add_column(u'survey_commutersurvey', 'caltdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.bdays'
        db.add_column(u'survey_commutersurvey', 'bdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.odays'
        db.add_column(u'survey_commutersurvey', 'odays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.outsidechanges'
        db.add_column(u'survey_commutersurvey', 'outsidechanges',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cpdaysaway'
        db.add_column(u'survey_commutersurvey', 'cpdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.from_work_switch'
        db.add_column(u'survey_commutersurvey', 'from_work_switch',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Commutersurvey.lastweek'
        db.add_column(u'survey_commutersurvey', 'lastweek',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.rdaysaway'
        db.add_column(u'survey_commutersurvey', 'rdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cdaysaway'
        db.add_column(u'survey_commutersurvey', 'cdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.health'
        db.add_column(u'survey_commutersurvey', 'health',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.odaysaway'
        db.add_column(u'survey_commutersurvey', 'odaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.caltdaysaway'
        db.add_column(u'survey_commutersurvey', 'caltdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tdays'
        db.add_column(u'survey_commutersurvey', 'tdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.height'
        db.add_column(u'survey_commutersurvey', 'height',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.bdaysaway'
        db.add_column(u'survey_commutersurvey', 'bdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.gender'
        db.add_column(u'survey_commutersurvey', 'gender',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tcdaysaway'
        db.add_column(u'survey_commutersurvey', 'tcdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.gender_other'
        db.add_column(u'survey_commutersurvey', 'gender_other',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.affectedyou'
        db.add_column(u'survey_commutersurvey', 'affectedyou',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.weight'
        db.add_column(u'survey_commutersurvey', 'weight',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.wdays'
        db.add_column(u'survey_commutersurvey', 'wdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.wdaysaway'
        db.add_column(u'survey_commutersurvey', 'wdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tdaysaway'
        db.add_column(u'survey_commutersurvey', 'tdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.to_work_switch'
        db.add_column(u'survey_commutersurvey', 'to_work_switch',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Commutersurvey.tcdays'
        db.add_column(u'survey_commutersurvey', 'tcdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.rdays'
        db.add_column(u'survey_commutersurvey', 'rdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cdays'
        db.add_column(u'survey_commutersurvey', 'cdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'survey.commutersurvey': {
            'Meta': {'object_name': 'Commutersurvey'},
            'already_green': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calorie_change': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'carbon_change': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'change_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Employer']", 'null': 'True'}),
            'employer_legacy': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'mode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Mode']", 'null': 'True', 'blank': 'True'})
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