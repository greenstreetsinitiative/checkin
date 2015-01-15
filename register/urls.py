from django.conf.urls import patterns, url
from django.conf import settings
from register import views

urlpatterns = patterns('',
    url(r'^$', views.register, name='index'),
    url(r'^post/?$', views.form_submission, name='form'),
)
