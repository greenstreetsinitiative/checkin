# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Month'
        db.delete_table(u'leaderboard_month')


    def backwards(self, orm):
        # Adding model 'Month'
        db.create_table(u'leaderboard_month', (
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('url_month', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'leaderboard', ['Month'])


    models = {
        
    }

    complete_apps = ['leaderboard']