# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Month'
        db.create_table(u'leaderboard_month', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            ('url_month', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal(u'leaderboard', ['Month'])


    def backwards(self, orm):
        # Deleting model 'Month'
        db.delete_table(u'leaderboard_month')


    models = {
        u'leaderboard.month': {
            'Meta': {'object_name': 'Month'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'url_month': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['leaderboard']