from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^walkboston/', include('walkboston.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Translation app
    (r'^rosetta/', include('rosetta.urls')),
    
    # school list
    (r'^$', 'walkboston.survey.views.index'),
    
    # survey form
    (r'^(?P<school_slug>[-\w]+)/$', 'walkboston.survey.views.form'),    
    
)


