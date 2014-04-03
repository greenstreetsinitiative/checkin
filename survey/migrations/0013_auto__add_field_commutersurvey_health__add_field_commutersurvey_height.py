# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Commutersurvey.health'
        db.add_column(u'survey_commutersurvey', 'health',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.height'
        db.add_column(u'survey_commutersurvey', 'height',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.gender'
        db.add_column(u'survey_commutersurvey', 'gender',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.gender_other'
        db.add_column(u'survey_commutersurvey', 'gender_other',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cdays'
        db.add_column(u'survey_commutersurvey', 'cdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.caltdays'
        db.add_column(u'survey_commutersurvey', 'caltdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cpdays'
        db.add_column(u'survey_commutersurvey', 'cpdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tdays'
        db.add_column(u'survey_commutersurvey', 'tdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.bdays'
        db.add_column(u'survey_commutersurvey', 'bdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.rdays'
        db.add_column(u'survey_commutersurvey', 'rdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.wdays'
        db.add_column(u'survey_commutersurvey', 'wdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.odays'
        db.add_column(u'survey_commutersurvey', 'odays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tcdays'
        db.add_column(u'survey_commutersurvey', 'tcdays',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.lastweek'
        db.add_column(u'survey_commutersurvey', 'lastweek',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cdaysaway'
        db.add_column(u'survey_commutersurvey', 'cdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.caltdaysaway'
        db.add_column(u'survey_commutersurvey', 'caltdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.cpdaysaway'
        db.add_column(u'survey_commutersurvey', 'cpdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tdaysaway'
        db.add_column(u'survey_commutersurvey', 'tdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.bdaysaway'
        db.add_column(u'survey_commutersurvey', 'bdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.rdaysaway'
        db.add_column(u'survey_commutersurvey', 'rdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.wdaysaway'
        db.add_column(u'survey_commutersurvey', 'wdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.odaysaway'
        db.add_column(u'survey_commutersurvey', 'odaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.tcdaysaway'
        db.add_column(u'survey_commutersurvey', 'tcdaysaway',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.outsidechanges'
        db.add_column(u'survey_commutersurvey', 'outsidechanges',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.affectedyou'
        db.add_column(u'survey_commutersurvey', 'affectedyou',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Commutersurvey.contact'
        db.add_column(u'survey_commutersurvey', 'contact',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Commutersurvey.volunteer'
        db.add_column(u'survey_commutersurvey', 'volunteer',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Commutersurvey.weight'
        db.alter_column(u'survey_commutersurvey', 'weight', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):
        # Deleting field 'Commutersurvey.health'
        db.delete_column(u'survey_commutersurvey', 'health')

        # Deleting field 'Commutersurvey.height'
        db.delete_column(u'survey_commutersurvey', 'height')

        # Deleting field 'Commutersurvey.gender'
        db.delete_column(u'survey_commutersurvey', 'gender')

        # Deleting field 'Commutersurvey.gender_other'
        db.delete_column(u'survey_commutersurvey', 'gender_other')

        # Deleting field 'Commutersurvey.cdays'
        db.delete_column(u'survey_commutersurvey', 'cdays')

        # Deleting field 'Commutersurvey.caltdays'
        db.delete_column(u'survey_commutersurvey', 'caltdays')

        # Deleting field 'Commutersurvey.cpdays'
        db.delete_column(u'survey_commutersurvey', 'cpdays')

        # Deleting field 'Commutersurvey.tdays'
        db.delete_column(u'survey_commutersurvey', 'tdays')

        # Deleting field 'Commutersurvey.bdays'
        db.delete_column(u'survey_commutersurvey', 'bdays')

        # Deleting field 'Commutersurvey.rdays'
        db.delete_column(u'survey_commutersurvey', 'rdays')

        # Deleting field 'Commutersurvey.wdays'
        db.delete_column(u'survey_commutersurvey', 'wdays')

        # Deleting field 'Commutersurvey.odays'
        db.delete_column(u'survey_commutersurvey', 'odays')

        # Deleting field 'Commutersurvey.tcdays'
        db.delete_column(u'survey_commutersurvey', 'tcdays')

        # Deleting field 'Commutersurvey.lastweek'
        db.delete_column(u'survey_commutersurvey', 'lastweek')

        # Deleting field 'Commutersurvey.cdaysaway'
        db.delete_column(u'survey_commutersurvey', 'cdaysaway')

        # Deleting field 'Commutersurvey.caltdaysaway'
        db.delete_column(u'survey_commutersurvey', 'caltdaysaway')

        # Deleting field 'Commutersurvey.cpdaysaway'
        db.delete_column(u'survey_commutersurvey', 'cpdaysaway')

        # Deleting field 'Commutersurvey.tdaysaway'
        db.delete_column(u'survey_commutersurvey', 'tdaysaway')

        # Deleting field 'Commutersurvey.bdaysaway'
        db.delete_column(u'survey_commutersurvey', 'bdaysaway')

        # Deleting field 'Commutersurvey.rdaysaway'
        db.delete_column(u'survey_commutersurvey', 'rdaysaway')

        # Deleting field 'Commutersurvey.wdaysaway'
        db.delete_column(u'survey_commutersurvey', 'wdaysaway')

        # Deleting field 'Commutersurvey.odaysaway'
        db.delete_column(u'survey_commutersurvey', 'odaysaway')

        # Deleting field 'Commutersurvey.tcdaysaway'
        db.delete_column(u'survey_commutersurvey', 'tcdaysaway')

        # Deleting field 'Commutersurvey.outsidechanges'
        db.delete_column(u'survey_commutersurvey', 'outsidechanges')

        # Deleting field 'Commutersurvey.affectedyou'
        db.delete_column(u'survey_commutersurvey', 'affectedyou')

        # Deleting field 'Commutersurvey.contact'
        db.delete_column(u'survey_commutersurvey', 'contact')

        # Deleting field 'Commutersurvey.volunteer'
        db.delete_column(u'survey_commutersurvey', 'volunteer')


        # Changing field 'Commutersurvey.weight'
        # FIXME: needs routine to cast VARCHAR to NUMERIC
        # db.alter_column(u'survey_commutersurvey', 'weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=1))

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
            'legs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Leg']", 'symmetrical': 'False'}),
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
            'day': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['survey']